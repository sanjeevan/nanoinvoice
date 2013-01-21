from flask.ext.wtf import (Form, HiddenField, DecimalField, TextField,
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
    type_id         = SelectField(u'Type', coerce=int, validators=[required()])
    tax_rate_id     = SelectField(u'Tax rate', coerce=int)
    description     = TextField(u'Description', validators=[required()])
    quantity        = DecimalField(u'Quantity')
    price           = DecimalField(u'Price', default=0)

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(InvoiceItemForm, self).__init__(formdata, obj, prefix, kwargs)

        self.type_id.choices = self.get_type_options()
        self.tax_rate_id.choices = self.get_tax_rate_options()
        if obj:
            self.model = obj
        else:
            self.model = None
            self.price.default = 0
            self.price.process(formdata)
    
    def validate_quantity(form, field):
        """Comments don't require a price, everything else does"""
        item_type = InvoiceItemType.query.get(form.type_id.data)
        if item_type.name == 'Comment':
            field.data = 0
        else:
            if field.data == None:
                raise ValidationError('Quantity must be supplied')
    
    def validate_price(form, field):
        """Comments don't require a price, everything else does"""
        item_type = InvoiceItemType.query.get(form.type_id.data)
        if item_type.name == 'Comment':
            field.data = 0
        else:
            if field.data == None:
                raise ValidationError('Price must be supplied')

    def get_type_options(self):
        """Get item types"""
        options = []
        types = InvoiceItemType.query.order_by('sort_order asc').all()
        for t in types:
            options.append((t.id, t.name))
        return options

    def get_tax_rate_options(self):
        """Get all tax rates"""
        options = []
        tax_rates = TaxRate.query.filter_by(user_id=current_user.id).all()
        for rate in tax_rates:
            options.append((rate.id, rate.name))
        options.append((-1, 'None'))
        return options

    def save(self):
        """Save new invoice item"""
        invoice = Invoice.query.get(self.invoice_id.data) 

        if not self.model:
            item = InvoiceItem()
        else:
            item = self.model

        item.invoice_id = self.invoice_id.data
        item.type_id = self.type_id.data
        if (self.tax_rate_id.data != -1):
            item.tax_rate_id = self.tax_rate_id.data
        item.description = self.description.data
        item.quantity = float(self.quantity.data)
        item.price = float(self.price.data)
        item.sort_order = invoice.next_item_sort_order()
        item.update_totals()

        db.session.add(item)
        db.session.commit()

        return item


