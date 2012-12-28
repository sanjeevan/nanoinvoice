from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          SubmitField, PasswordField, FormField,
                          ValidationError, required, equal_to, email,
                          length)
from flaskext.babel import gettext, lazy_gettext as _
from flask.ext.login import current_user 

from nano.extensions import db

class UserForm(Form):
    first_name          = TextField(u'First name', validators=[required()])
    last_name           = TextField(u'Last name', validators=[required()])
    email_address       = TextField(u'Email address', validators=[required()])
    password            = PasswordField(u'New password')
    password_confirm   = PasswordField(u'Password confirm')
