"""This is the client login portal

    Requests are routed via a subdomain in the format:
        
        [username].nanoinvoice.com
"""
import uuid
import gocardless
import gocardless.client

from gocardless.client import Client
from flask import Blueprint, render_template, redirect, url_for, current_app, request

from nano.models import User, GoCardlessAccount, InvoiceLink, GoCardlessPayment, Payment
from nano.extensions import db

portal = Blueprint('portal', __name__, url_prefix='/portal')

@portal.route('/', methods=['GET'], subdomain='<username>')
def index(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return 'Invalid account', 404
    return render_template('portal/index.html', subdomain=username)

@portal.route('/invoice/<string:paylink>', methods=['GET'], subdomain='<username>')
def invoice(username, paylink):
    user = User.query.filter_by(username=username).first()
    if not user:
        return 'Invalid account', 404

    invoice_link = InvoiceLink.query.filter_by(user_id=user.id) \
                                    .filter_by(link=paylink) \
                                    .first()

    if not invoice_link:
        return 'Invalid invoice', 404

    company             = invoice_link.user.company
    stripe_account      = invoice_link.user.stripe_account
    gocardless_account  = invoice_link.user.gocardless_account

    return render_template('portal/invoice.html', invoice=invoice_link.invoice,
                                                  invoice_link=invoice_link,
                                                  stripe=stripe_account,
                                                  gocardless=gocardless_account,
                                                  company=company,
                                                  user=user,
                                                  page_title='Invoice from %s' % user.company.name)


@portal.route('/gocardless/pay/<string:paylink>', methods=['GET', 'POST'], subdomain='<username>')
def gocardless_pay(username, paylink):
    user = User.query.filter_by(username=username).first()
    if not user:
        return 'Invalid account', 404

    invoice_link = InvoiceLink.query.filter_by(user_id=user.id) \
                                    .filter_by(link=paylink) \
                                    .first()

    if not invoice_link:
        return 'Invalid invoice', 404

    invoice = invoice_link.invoice
    gocardless_account = GoCardlessAccount.get_or_create_for_user(user.id)
    if not gocardless_account.enabled:
        return 'GoCardless integration is not enabled for this account', 400

    gocardless.environment = current_app.config['GOCARDLESS_ENVIRONMENT']
    client = Client(gocardless_account.app_identifier,
                    app_secret=gocardless_account.app_secret.encode('utf-8'),
                    access_token=gocardless_account.merchant_access_token.encode('utf-8'),
                    merchant_id=gocardless_account.merchant_id.encode('utf-8'))

    gocardless_payment = GoCardlessPayment()
    gocardless_payment.invoice_id = invoice.id
    gocardless_payment.user_id = user.id
    gocardless_payment.reference = uuid.uuid4()
    gocardless_payment.amount = invoice.total
    db.session.add(gocardless_payment)
    db.session.commit()

    redirect_url = url_for('portal.gocardless_success', reference=gocardless_payment.reference, 
                                                        username=user.username,
                                                        _external=True)
    cancel_url = url_for('portal.invoice', username=user.username,
                                           paylink=paylink,
                                           cancel='yes',
                                           _external=True)

    url = client.new_bill_url(invoice.total,
                              name='Invoice %s for %s' % (invoice.reference, invoice.contact.organisation),
                              redirect_uri=redirect_url,
                              cancel_uri=cancel_url)

    return redirect(url)

@portal.route('/gocardless/pay/success', methods=['GET'], subdomain='<username>')
def gocardless_success(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return 'Invalid account', 404

    gocardless_payment = GoCardlessPayment.query.filter_by(reference=request.args.get('reference')).first()
    if not gocardless_payment:
        return 'Not a valid payment', 404

    param_keys = ['resource_uri', 'resource_id', 'resource_type', 'signature', 'state']
    params = {}
    for key in param_keys:
        val = request.args.get(key)
        if val:
            params[key] = val.encode('utf-8')

    gocardless_account = GoCardlessAccount.get_or_create_for_user(user.id)
    if not gocardless_account.enabled:
        return 'GoCardless integration is not enabled for this account', 400

    gocardless.environment = current_app.config['GOCARDLESS_ENVIRONMENT']
    client = Client(gocardless_account.app_identifier,
                    app_secret=gocardless_account.app_secret.encode('utf-8'),
                    access_token=gocardless_account.merchant_access_token.encode('utf-8'),
                    merchant_id=gocardless_account.merchant_id.encode('utf-8'))

    try:
        client.confirm_resource(params)
    except Exception as e:
        return render_template('portal/gocardless_error.html', user=user, exception=e)

    payment = Payment()
    payment.invoice_id = gocardless_payment.invoice_id
    payment.amount = gocardless_payment.amount
    payment.currency_code = gocardless_payment.invoice.currency_code
    payment.method = 'Direct Debit via Gocardless'
    db.session.add(payment)
    db.session.commit() 

    gocardless_payment.state = u'confirmed'
    gocardless_payment.payment_id = payment.id

    db.session.add(gocardless_payment)
    db.session.commit()

    payment.invoice.update_payment_status()

    return render_template('portal/gocardless_success.html', gocardless_payment=gocardless_payment)
