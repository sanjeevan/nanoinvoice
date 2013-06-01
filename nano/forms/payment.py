from datetime import datetime
from flask.ext.wtf import (Form, HiddenField, TextField, FormField,
                          DecimalField, ValidationError, required, equal_to, 
                          email, length, FormField, FieldList, optional)
from nano.extensions import db

class PaymentForm(Form):
    """Form for a new custom field"""
    
    DATE_FORMAT = '%a %b %d %Y'

    invoice_id  = HiddenField()
    amount      = TextField('Amount', [required()])
    method      = TextField()
    date        = TextField('Date', [required()])
    
    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(PaymentForm, self).__init__(formdata, obj, prefix, kwargs)
        if obj is not None:
            self.payment = obj
        else:
            self.payment = None

    def save(self):
        """Save the payment model"""
        self.payment.amount = self.amount.data
        self.payment.date = datetime.strptime(self.date.data, self.DATE_FORMAT)
        self.payment.method = self.method.data

        db.session.add(self.payment)
        db.session.commit()

        self.payment.invoice.update_payment_status()

        return self.payment

class PaymentIntegrationForm(Form):
    """Payments integration"""

    pass
