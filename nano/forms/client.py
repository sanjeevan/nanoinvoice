from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          PasswordField, SubmitField,
                          ValidationError, required, equal_to, email,
                          length)
from flaskext.babel import gettext, lazy_gettext as _


class SimpleClientForm(Form):
    first_name      = TextField(u'First name')
    last_name       = TextField(u'Last name')
    email_address   = TextField(u'Email address')

class DetailedClientForm(Form):
    basic           = FormField(SimpleClientForm)
    org             = TextField(u'Organisation')
    
