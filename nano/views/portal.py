"""This is the client login portal

    Requests are routed via a subdomain in the format:
        
        [username].nanoinvoice.com
"""
import uuid
import stripe
import gocardless
import gocardless.client

from gocardless.client import Client
from flask import (Blueprint, render_template, redirect, url_for, current_app, 
                   request, flash)

from nano.models import (User, InvoiceLink, Payment,
                         GoCardlessPayment, GoCardlessAccount,
                         StripeAccount, StripePayment)
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
    stripe_account      = StripeAccount.get_or_create_for_user(user.id)
    gocardless_account  = GoCardlessAccount.get_or_create_for_user(user.id)

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
                                                        paylink=paylink,
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
    paylink = request.args.get('paylink')
    reference = request.args.get('reference')
    user = User.query.filter_by(username=username).first()
    if not user:
        return 'Invalid account', 404

    gocardless_payment = GoCardlessPayment.query.filter_by(reference=reference).first()
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

        payment = gocardless_payment.create_payment_object()
        payment.invoice.update_payment_status()

        gocardless_payment.state = u'confirmed'
        gocardless_payment.payment_id = payment.id
        gocardless_payment.resource_id = request.args.get('resource_id')
        gocardless_payment.resource_uri = request.args.get('resource_uri')

        db.session.add(gocardless_payment)
        db.session.commit()

    except Exception as e:
        gocardless_payment.state = u'error'
        gocardless_payment.error_message = e.message
        db.session.add(gocardless_payment)
        db.session.commit()
        return render_template('portal/gocardless_error.html', user=user, exception=e)

    flash('Payment was successful')
    return redirect(url_for('portal.invoice', paylink=paylink, username=username))

@portal.route('/stripe/pay/<string:paylink>', methods=['POST'], subdomain='<username>')
def stripe_pay(username, paylink):
    """The stripe.js file will post credit card data"""
    user = User.query.filter_by(username=username).first()
    if not user:
        return 'Invalid account', 404

    invoice_link = InvoiceLink.query.filter_by(user_id=user.id) \
                                    .filter_by(link=paylink) \
                                    .first()
    if not invoice_link:
        return 'Invalid invoice', 404
    
    if not request.form['stripe_token']:
        return 'Stripe token not present', 400

    stripe_account = StripeAccount.get_or_create_for_user(user.id)
    stripe.api_key = stripe_account.secret_key

    stripe_payment = StripePayment()
    stripe_payment.invoice_id = invoice_link.invoice_id
    stripe_payment.amount = invoice_link.invoice.total
    stripe_payment.user_id = user.id
    stripe_payment.token = request.form['stripe_token']

    db.session.add(stripe_payment)
    db.session.commit()

    # Create the charge on Stripe's servers - this will charge the user's card
    try:
        pence = int(stripe_payment.amount * 100)
        charge = stripe.Charge.create(
            amount=pence, # amount in cents, again
            currency=invoice_link.invoice.currency_code.lower(),
            card=request.form['stripe_token'],
            description='Invoice reference: %s' % invoice_link.invoice.reference
        )

        payment = stripe_payment.create_payment_object()
        payment.invoice.update_payment_status()
        
        stripe_payment.state = u'confirmed'
        stripe_payment.charge_id = charge.id
        stripe_payment.charge = str(charge)
        stripe_payment.payment_id = payment.id

        db.session.commit()
    except Exception, e:
        # The card has been declined
        stripe_payment.state = 'error'
        stripe_payment.error_message = e.message
        db.session.commit()
        return 'There was an error', 400
        
    flash('Payment was successful')
    return redirect(url_for('portal.invoice', paylink=paylink, username=username)) 
