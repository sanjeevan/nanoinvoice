from flask.ext.wtf import (Form, HiddenField, TextField, FormField,
                          ValidationError, required, equal_to, email,
                          length, FormField, FieldList, optional)
from flaskext.babel import gettext, lazy_gettext as _
from flask.ext.login import current_user 

from nano.models import CustomField
from nano.extensions import db
from nano.utils import Struct

class CustomFieldForm(Form):
    """Form for existing custom fields already created"""
    
    uid         = HiddenField(u'ID', [required()])
    field_name  = TextField(u'Name', [required()])
    field_value = TextField(u'Value', [required()])

    def save(self):
        obj = CustomField.query.get(self.uid.data)
        obj.name = self.field_name.data
        obj.value = self.field_value.data
        db.session.add(obj)
        db.session.commit()
        

class NewCustomFieldForm(Form):
    """Form for a new custom field"""

    field_name      = TextField(u'Name', validators=[optional()])
    field_value     = TextField(u'Value', validators=[optional()])                

    def validate_field_name(form, field):
        if field.data and not form.field_value.data:
            raise ValidationError('Please specify a value')

    def validate_field_value(form, field):
        if field.data and not form.field_name.data:
            raise ValidationError('Please name this field')
    
    def save_if_data(self):
        if self.field_name.data and self.field_value.data:
            custom_field = CustomField()
            custom_field.user_id = current_user.id
            custom_field.name = self.field_name.data
            custom_field.value = self.field_value.data
            db.session.add(custom_field)
            db.session.commit()
            return custom_field
        else:
            return None

class CustomFieldsManagementForm(Form):
    """Acts as a container for managing the custom field forms"""
    
    current_fields = FieldList(FormField(CustomFieldForm))
    new_field      = FormField(NewCustomFieldForm)
     
    @classmethod
    def transform(cls, custom_fields):
        container = Struct(current_fields=[])

        for model in custom_fields:
            obj = Struct(uid=model.id, field_name=model.name, field_value=model.value)
            container.current_fields.append(obj)
        return container
    
    def save(self):
        # save existing fields
        for custom_form in self.current_fields:
            custom_form.save()
        
        self.new_field.save_if_data()
