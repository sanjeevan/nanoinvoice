from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          PasswordField, SubmitField, FormField,
                          ValidationError, required, equal_to, email,
                          length)
from flaskext.babel import gettext, lazy_gettext as _

class ClientAddress(Form):
    address_line1   = TextField(u'Address Line 1') 
    address_line2   = TextField(u'Address Line 2') 

class SimpleClientForm(Form):
    first_name      = TextField(u'First name', validators=[required()])
    last_name       = TextField(u'Last name', validators=[required()])
    email_address   = TextField(u'Email address', validators=[required()])

class DetailedClientForm(Form):
    basic           = FormField(SimpleClientForm)
    org             = TextField(u'Organisation')
    address         = FormField(ClientAddress)
