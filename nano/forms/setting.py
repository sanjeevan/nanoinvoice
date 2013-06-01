"""Settings form"""

from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          SubmitField, SelectField, FormField, TextAreaField,
                          ValidationError, required, equal_to, email,
                          length)

from nano.extensions import db
from nano.models import CompanyType, Country

class SettingForm(Form):
    
    email_template = TextAreaField('Email template', [required()])

    def save(self, user):
        user.setting.set_val('email_template', self.email_template.data)
        return True
