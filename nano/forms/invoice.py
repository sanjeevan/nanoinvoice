from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          PasswordField, SubmitField, FormField, SelectField,
                          ValidationError, required, equal_to, email,
                          length)
from flaskext.babel import gettext, lazy_gettext as _

from nano.models import Contact, PaymentTerm, Invoice, Currency
from nano.extensions import db
from flask.ext.login import current_user 
from datetime import datetime, timedelta

class InvoiceForm(Form):

    # Sun Nov 25 2012
    DATE_FORMAT = '%a %b %d %Y'

    contact_id      = SelectField(u'Clients', coerce=int, validators=[required()])
    reference       = TextField(u'Reference', validators=[required()])
    payment_term_id = SelectField(u'Payment terms', coerce=int, validators=[required()])
    date_issued     = TextField(u'Date issued', validators=[required()])
    due_date        = TextField(u'Due date')
    currency_code      = SelectField(u'Currency', validators=[required()])

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(InvoiceForm, self).__init__(formdata, obj, prefix, kwargs)
        
        if obj:
            self.invoice = obj
            self.date_issued.data = obj.date_issued.strftime(self.DATE_FORMAT)
            self.due_date.data = obj.due_date.strftime(self.DATE_FORMAT)
        else:
            self.invoice = None
            self.date_issued.data = datetime.now().strftime(self.DATE_FORMAT)

        self.contact_id.choices = self.get_contact_options()
        self.payment_term_id.choices = self.get_payment_term_options()
        self.reference.data = Invoice.next_invoice_number(current_user)
        self.currency_code.choices = self.get_currency_options()
    
    def get_currency_options(self):
        options = []
        currencies = Currency.query.all()
        for currency in currencies:
            label = '%s (%s)' % (currency.name, currency.symbol)
            options.append((str(currency.code), label))
        return options

    def get_payment_term_options(self):
        terms = PaymentTerm.query.all()
        options = [(term.id, term.name) for term in terms]
        return options

    def get_contact_options(self):
        options = []
        contacts = Contact.query.filter_by(user_id=current_user.id).all()
        for contact in contacts:
            options.append((contact.id, contact.first_name + ' ' + contact.last_name))
        return options

    def save(self):
        if not self.invoice:
            invoice = Invoice()
            invoice.status = 'draft'
        else:
            invoice = self.invoice

        invoice.user_id = current_user.id
        invoice.contact_id = self.contact_id.data
        invoice.reference = self.reference.data
        invoice.currency_code = self.currency_code.data
        invoice.date_issued = datetime.strptime(self.date_issued.data, self.DATE_FORMAT)
        
        payment_term = PaymentTerm.query.get(self.payment_term_id.data)
        invoice.payment_term_id = payment_term.id

        if payment_term.days == -1:
            invoice.due_date = datetime.strptime(self.due_date.data, self.DATE_FORMAT)
        else:
            now = datetime.now()
            invoice.due_date = now + timedelta(days=payment_term.days) 
        
        invoice.update_totals()

        db.session.add(invoice)
        db.session.commit()
        return invoice

