from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          SelectField, SubmitField, FormField,
                          ValidationError, required, equal_to, email,
                          length)
from flaskext.babel import gettext, lazy_gettext as _

from nano.models import Contact, Country
from nano.extensions import db
from flask.ext.login import current_user 

class ClientAddress(Form):
    address_line1   = TextField(u'Address Line 1') 
    address_line2   = TextField(u'Address Line 2') 

class SimpleClientForm(Form):
    """Used when a client is first created"""

    first_name      = TextField(u'First name', validators=[required()])
    last_name       = TextField(u'Last name', validators=[required()])
    email_address   = TextField(u'Email address', validators=[required()])

    def save(self):
        client = Contact()
        client.user_id = current_user.id
        client.first_name = self.first_name.data
        client.last_name = self.last_name.data
        client.email_address = self.email_address.data
        
        db.session.add(client)
        db.session.commit()

        return client

class DetailedClientForm(Form):

    first_name      = TextField(u'First name', validators=[required()])
    last_name       = TextField(u'Last name', validators=[required()])
    email_address   = TextField(u'Email address', validators=[required()])
    organisation    = TextField(u'Company', validators=[required()])
    
    billing_email_address = TextField(u'Billing email address', validators=[])
    address_line1   = TextField(u'Street address', validators=[])
    address_line2   = TextField(u'', validators=[])
    town            = TextField(u'Town', validators=[])
    city            = TextField(u'City', validators=[])
    county          = TextField(u'County', validators=[])
    country         = SelectField(u'Country', coerce=unicode, validators=[])
    post_code       = TextField(u'Post code', validators=[])

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(DetailedClientForm, self).__init__(formdata, obj, prefix, **kwargs)
        if obj is not None:
            self.contact = obj
        else:
            self.contact = None


        self.country.choices = self.get_country_options()
    
    def get_country_options(self):
        choices = []
        countries = Country.query.order_by('name asc').all()
        for country in countries:
            choices.append((country.iso, country.printable_name))
        return choices 
    
    def save(self):
        self.populate_obj(self.contact)

        db.session.add(self.contact)
        db.session.commit()

