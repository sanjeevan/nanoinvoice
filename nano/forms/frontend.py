from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          PasswordField, SubmitField, TextField, SelectField,
                          ValidationError, required, equal_to, email,
                          length)
from flaskext.babel import gettext, lazy_gettext as _

from nano.models import User, Company, CompanyType, Country
from nano.extensions import db


class LoginForm(Form):
    next = HiddenField()
    remember = BooleanField(_('Remember me'))
    login = TextField(_('Username or email address'), [required()])
    password = PasswordField(_('Password'), [required(), length(min=6, max=16)])
    submit = SubmitField(_('Login'))

class SignupForm(Form):
    next = HiddenField()

    first_name      = TextField('First name', [required('Your first name is required')])
    last_name       = TextField('Last name', [required('Your last name is required')])
    username        = TextField(_('Username'), [required('Please enter a valid subdomain for your account')])
    business_name   = TextField(_('Business name'), [required('Please supply a business name')])
    business_type   = SelectField('Company type', [required('Please supply the type of company')])
    password        = PasswordField(_('Password'), [required('Please enter a password'), length(min=6, max=16)])
    password_again  = PasswordField(_('Password again'), [required('Please confirm your password'), length(min=6, max=16), equal_to('password')])
    email_address   = TextField(_('Email address'), [required('Your email address is required'), email(message=_('A valid email address is required'))])
    country_id      = SelectField('Country', [required('Please select a country')])

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(SignupForm, self).__init__(formdata, obj, prefix, kwargs)
        self.business_type.choices = self.get_company_type_options()
        self.country_id.choices = self.get_country_options()

    def get_country_options(self):
        """Get options for country list"""
        choices = []
        countries = Country.query.all()
        for country in countries:
            choices.append((country.iso, country.printable_name))
        return choices 

    def get_company_type_options(self):
        choices = []
        types = CompanyType.query.all()
        for t in types:
            choices.append((str(t.id), t.name))
        return choices

    def save(self):
        """Create a new user account"""

        user = User()
        user.username = self.username.data
        user.first_name = self.first_name.data
        user.last_name = self.last_name.data
        user.email_address = self.email_address.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()

        company = Company()
        company.user_id = user.id
        company.name = self.business_name.data
        company.company_type_id = self.business_type.data
        company.country = self.country_id.data
        db.session.add(company)
        db.session.commit()

        return user

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError, gettext('This subdomain is already taken')

    def validate_email_address(self, field):
        if User.query.filter_by(email_address=field.data).first() is not None:
            raise ValidationError, gettext('This email address is taken')


class RecoverPasswordForm(Form):
    email = TextField(_('Your email'), validators=[
                      email(message=_('A valid email address is required'))])
    submit = SubmitField(_('Send instructions'))


class ChangePasswordForm(Form):
    activation_key = HiddenField()
    password = PasswordField('Password', validators=[
                             required(message=_('Password is required'))])
    password_again = PasswordField(_('Password again'), validators=[
                                   equal_to('password', message=\
                                            _("Passwords don't match"))])
    submit = SubmitField(_('Save'))


class ReauthForm(Form):
    next = HiddenField()
    password = PasswordField(_('Password'), [required(), length(min=6, max=16)])
    submit = SubmitField(_('Reauthenticate'))

