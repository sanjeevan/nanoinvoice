from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          PasswordField, SubmitField, FormField, SelectField,
                          ValidationError, required, equal_to, email,
                          length)
from flaskext.babel import gettext, lazy_gettext as _

from nano.models import Contact, PaymentTerm, Invoice
from nano.extensions import db
from flask.ext.login import current_user 
from datetime import datetime, timedelta

class InvoiceForm(Form):

    # Sun Nov 25 2012
    DATE_FORMAT = '%a %b %d %Y'

    contact_id      = SelectField(u'Clients', validators=[required()])
    reference       = TextField(u'Reference', validators=[required()])
    payment_term_id = SelectField(u'Payment terms', validators=[required()])
    date_issued     = TextField(u'Date issued', validators=[required()])
    due_date        = TextField(u'Due date')

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):

        super(InvoiceForm, self).__init__(formdata, obj, prefix, kwargs)
        
        self.contact_id.choices = self.get_contact_options()
        self.payment_term_id.choices = self.get_payment_term_options()
        self.reference.data = Invoice.next_invoice_number(current_user)
        self.date_issued.data = datetime.now().strftime(self.DATE_FORMAT)

    def get_payment_term_options(self):
        terms = PaymentTerm.query.all()
        options = [(str(term.days), term.name) for term in terms]
        return options

    def get_contact_options(self):
        options = []
        contacts = Contact.query.filter_by(user_id=current_user.id).all()
        for contact in contacts:
            options.append((str(contact.id), contact.first_name + ' ' + contact.last_name))
        return options

    def save(self):
        invoice = Invoice()
        invoice.user_id = current_user.id
        invoice.contact_id = self.contact_id.data
        invoice.status = 'new'
        invoice.reference = self.reference.data
        invoice.currency_code = 'GBP'
        invoice.date_issued = datetime.strptime(self.date_issued.data, self.DATE_FORMAT)
        
        payment_term = PaymentTerm.query.filter_by(days=self.payment_term_id.data).first()
        invoice.payment_term_id = payment_term.id

        if int(self.payment_term_id.data) == -1:
            invoice.due_date = datetime.strptime(self.due_date.data, self.DATE_FORMAT)
        else:
            now = datetime.now()
            days = int(self.payment_term_id.data)
            invoice.due_date = now + timedelta(days=days) 
        
        invoice.update_totals()

        db.session.add(invoice)
        db.session.commit()
        return invoice

