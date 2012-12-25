from flask.ext.wtf import (Form, HiddenField, FloatField, TextField,
                          IntegerField, SubmitField, FormField, SelectField,
                          ValidationError, required, equal_to, email,
                          length)
from flaskext.babel import gettext, lazy_gettext as _

from nano.models import Invoice, InvoiceItem, InvoiceItemType, TaxRate
from nano.extensions import db
from flask.ext.login import current_user 
from datetime import datetime, timedelta

class InvoiceItemForm(Form):

    invoice_id      = IntegerField(u'Invoice id', validators=[required()])
    type_id         = SelectField(u'Type', validators=[required()])
    tax_rate_id     = SelectField(u'Tax rate')
    description     = TextField(u'Description', validators=[required()])
    quantity        = IntegerField(u'Quantity', validators=[required()])
    price           = FloatField(u'Price', validators=[required()])

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(InvoiceItemForm, self).__init__(formdata, obj, prefix, kwargs)

        self.type_id.choices = self.get_type_options()
        self.tax_rate_id.choices = self.get_tax_rate_options()

    def get_type_options(self):
        """Get item types"""
        options = []
        types = InvoiceItemType.query.order_by('sort_order asc').all()
        for t in types:
            options.append((str(t.id), t.name))
        return options

    def get_tax_rate_options(self):
        """Get all tax rates"""
        options = []
        tax_rates = TaxRate.query.filter_by(user_id=current_user.id).all()
        for rate in tax_rates:
            options.append((str(rate.id), rate.name))
        return options

    def save(self):
        """Save new invoice item"""
        item = InvoiceItem()
        return item


