from flask.ext.wtf import (Form, TextField, PasswordField, FormField, required, 
                           EqualTo, Email, ValidationError, Optional)
from flask.ext.login import current_user 

from nano.models import User
from nano.extensions import db

class UserForm(Form):
    first_name          = TextField(u'First name', validators=[required()])
    last_name           = TextField(u'Last name', validators=[required()])
    email_address       = TextField(u'Email address', validators=[required(), Email()])
    password            = PasswordField(u'New password', validators=[Optional(), EqualTo('password_confirm')])
    password_confirm    = PasswordField(u'Password confirm', validators=[Optional()])

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(UserForm, self).__init__(formdata, obj, prefix, kwargs)
        if obj:
            self.user = obj
        else:
            self.user = None
    
    def validate_email_address(self, field):
        user = User.query.filter_by(email_address=field.data) \
                         .filter(User.id != self.user.id).first()
        if user:
            raise ValidationError('That email address is already in use')

    def save(self):
        self.user.first_name = self.first_name.data
        self.user.last_name = self.last_name.data
        self.user.email_address = self.email_address.data
        
        if len(self.password.data) > 1:
            self.user.password = self.password.data

        db.session.add(self.user)
        db.session.commit()
        return self.user
