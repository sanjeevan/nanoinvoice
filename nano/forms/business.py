from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          SubmitField, SelectField, FormField,
                          ValidationError, required, equal_to, email,
                          length)
from flaskext.babel import gettext, lazy_gettext as _
from flask.ext.login import current_user 

from nano.extensions import db

class BusinessForm(Form):
    """This actually maps more closely to the profile table"""
    
    company_type_id     = SelectField(u'Company type')
    company_name        = TextField(u'Company name')
    company_address1    = TextField(u'Address')
    company_address2    = TextField(u'')
    company_town        = TextField(u'City')
    company_county      = TextField(u'County/Province')
    company_post_code   = TextField(u'ZIP/Postal code')
    company_number      = TextField(u'Company registration no.')
    

    """
    first_name          = TextField(u'First name', validators=[required()])
    last_name           = TextField(u'Last name', validators=[required()])
    email_address       = TextField(u'Email address', validators=[required()])
    password            = PasswordField(u'New password')
    password_confirm   = PasswordField(u'Password confirm')
    """
