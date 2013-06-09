from datetime import datetime
from flask.ext.wtf import (Form, HiddenField, TextField, FormField, BooleanField,
                          DecimalField, ValidationError, required, equal_to, 
                          email, length, FormField, FieldList, optional)
from nano.extensions import db

class PaymentForm(Form):
    """Form for a new custom field"""
    
    DATE_FORMAT = '%a %b %d %Y'

    invoice_id  = HiddenField()
    amount      = TextField('Amount', [required()])
    description = TextField()
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
        self.payment.description = self.description.data

        db.session.add(self.payment)
        db.session.commit()

        self.payment.invoice.update_payment_status()

        return self.payment

class StripePaymentIntegrationForm(Form):
    """Stripe"""

    secret_key = TextField('Secret key')
    public_key = TextField('Public key')
    enabled = BooleanField('Enabled')

class GoCardlessPaymentIntegrationForm(Form):
    """Gocardless"""

    merchant_id           = TextField('Merchant Id')
    app_identifier        = TextField('App identifier')
    app_secret            = TextField('App secret')
    merchant_access_token = TextField('Merchant access token')
    enabled               = BooleanField('Enabled')

class PaymentIntegrationForm(Form):
    """Payments integration"""

    gocardless = FormField(GoCardlessPaymentIntegrationForm)
    stripe     = FormField(StripePaymentIntegrationForm)

    def __init__(self, formdata, obj=None, prefix='', **kwargs):
        super(PaymentIntegrationForm, self).__init__(formdata, obj, prefix, **kwargs)

        if obj:
            self.models = obj
        else:
            self.models = None

    def save(self):
        
        # gocardless
        self.models.gocardless.merchant_id = self.gocardless.merchant_id.data
        self.models.gocardless.merchant_access_token = self.gocardless.merchant_access_token.data
        self.models.gocardless.app_secret = self.gocardless.app_secret.data
        self.models.gocardless.app_identifier = self.gocardless.app_identifier.data
        self.models.gocardless.enabled = self.gocardless.enabled.data

        # stripe payments
        self.models.stripe.public_key = self.stripe.public_key.data
        self.models.stripe.secret_key = self.stripe.secret_key.data
        self.models.stripe.enabled = self.stripe.enabled.data

        db.session.commit()

