from flask.ext.wtf import (Form, HiddenField, TextField, FormField,
                          DecimalField, ValidationError, required, equal_to, 
                          email, length, FormField, FieldList, optional)
from flaskext.babel import gettext, lazy_gettext as _
from flask.ext.login import current_user 

from nano.models import TaxRate 
from nano.extensions import db
from nano.utils import Struct

class TaxRateForm(Form):
    """Form for existing custom fields already created"""
    
    uid       = HiddenField(u'ID', [required()])
    rate_name = TextField(u'Name', [required()])
    rate      = DecimalField(u'Value', places=2)

    def save(self):
        obj = TaxRate.query.get(self.uid.data)
        obj.name = self.rate_name.data
        obj.rate = self.rate.data
        db.session.add(obj)
        db.session.commit()
        

class NewTaxRateForm(Form):
    """Form for a new custom field"""

    rate_name = TextField(u'Name', validators=[optional()])
    rate      = DecimalField(u'Value', validators=[optional()], places=2)

    def save_if_data(self):
        if self.rate_name.data:
            if self.rate.data is None:
                rate = 0.00
            else:
                rate = float(self.rate.data)

            tax_rate = TaxRate()
            tax_rate.name = self.rate_name.data
            tax_rate.rate = rate
            tax_rate.user_id = current_user.id
            db.session.add(tax_rate)
            db.session.commit()
            return tax_rate
        else:
            return None

class TaxRateContainerForm(Form):
    """Acts as a container for managing the custom field forms"""
    
    current_taxes = FieldList(FormField(TaxRateForm))
    new_tax_rate  = FormField(NewTaxRateForm)
    
    @classmethod
    def to_form_data(cls, tax_rates=[]):
        container = Struct(current_taxes=[])
        for model in tax_rates:
            obj = Struct(uid=model.id, rate_name=model.name, rate=model.rate)
            container.current_taxes.append(obj)
        return container

    def save(self):
        # save existing fields
        for tax_rate_form in self.current_taxes:
            tax_rate_form.save()
        
        self.new_tax_rate.save_if_data()
