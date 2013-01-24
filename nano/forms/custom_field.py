from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          SelectField, SubmitField, FormField,
                          ValidationError, required, equal_to, email,
                          length)
from flaskext.babel import gettext, lazy_gettext as _

from nano.models import CustomField
from nano.extensions import db
from flask.ext.login import current_user 

class CustomFieldListForm(Form):
    pass

class CustomFieldForm(Form):

    field_name    = TextField(u'Name', validators=[required()])
    field_value   = TextField(u'Value', validators=[required()])

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(CustomFieldForm, self).__init__(formdata, obj, prefix, kwargs) 

    def save(self):
        cf = CustomField()
        cf.user_id = current_user.id
        cf.name = self.field_name.data
        cf.value = self.field_value.data

        db.session.add(cf)
        db.session.commit()
        return cf


