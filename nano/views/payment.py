"""Payment view"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.ext.login import login_required, current_user

from nano.forms import PaymentForm
from nano.models import Invoice, Payment
from nano.extensions import db

payment = Blueprint('payment', __name__, url_prefix='/payment')

@payment.route('/', methods=['GET'])
@login_required
def index():
    invoices = Invoice.query.filter_by(user_id=current_user.id).all()
    payments = Payment.query.filter(Payment.invoice_id.in_([i.id for i in invoices])) \
                            .order_by(Payment.date.asc()) \
                            .all()

    return render_template('payment/index.html', payments=payments)

@payment.route('/create/<int:invoice_id>', methods=['GET', 'POST'])
def create(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return 'Invoice not found', 404

    payment = Payment()
    payment.invoice_id = invoice.id
    payment.currency_code = invoice.currency_code
    
    form = PaymentForm(request.form, obj=payment)
    if request.method == 'POST' and form.validate():
        payment = form.save()
        flash('Payment added to invoice')
        return redirect(url_for('invoice.show', id=invoice.id))

    return render_template('payment/create.html', invoice=invoice, form=form)


@payment.route('/delete/<int:id>', methods=['GET'])
def edit(id):
    pass

@payment.route('/edit/<int:id>', methods=['GET', 'POST'])
def delete(id):
    """Delete a payment"""
    payment = Payment.query.get(id)
    if not payment:
        return 'Payment not found', 404

    invoice = payment.invoice
    db.session.delete(payment)
    db.session.commit()

    invoice.update_payment_status()

    flash('Payment deleted')
    return redirect(request.referrer)
