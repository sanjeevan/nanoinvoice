from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          PasswordField, SubmitField, FormField,
                          ValidationError, required, equal_to, email,
                          length)
from flaskext.babel import gettext, lazy_gettext as _

from nano.models import Contact
from nano.extensions import db
from flask.ext.login import current_user 

class ClientAddress(Form):
    address_line1   = TextField(u'Address Line 1') 
    address_line2   = TextField(u'Address Line 2') 

class SimpleClientForm(Form):
    first_name      = TextField(u'First name', validators=[required()])
    last_name       = TextField(u'Last name', validators=[required()])
    email_address   = TextField(u'Email address', validators=[required()])

    def save(self):
        print 'saving'
        client = Contact()
        client.user_id = current_user.id
        client.first_name = self.first_name.data
        client.last_name = self.last_name.data
        client.email_address = self.email_address.data
        
        db.session.add(client)
        db.session.commit()

        return client

class DetailedClientForm(Form):
    basic           = FormField(SimpleClientForm)
    org             = TextField(u'Organisation')
    address         = FormField(ClientAddress)

    def save(self):
        pass
