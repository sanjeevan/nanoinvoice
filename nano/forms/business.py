from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          SubmitField, SelectField, FormField,
                          ValidationError, required, equal_to, email,
                          length)

from nano.extensions import db
from nano.models import CompanyType, Country

class BusinessForm(Form):
    """This actually maps more closely to the profile table"""

    company_type_id     = SelectField(u'Company type', coerce=int, validators=[required()])
    name                = TextField(u'Company name', validators=[required()])
    address1            = TextField(u'Address', validators=[required()])
    address2            = TextField(u'')
    town                = TextField(u'Town', validators=[required()])
    city                = TextField(u'City', validators=[required()])
    county              = TextField(u'County/Province', validators=[required()])
    country             = SelectField(u'Country', coerce=unicode, validators=[required()]) 
    post_code           = TextField(u'ZIP/Postal code', validators=[required()])
    registration_no     = TextField(u'Company registration no.')

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(BusinessForm, self).__init__(formdata, obj, prefix, kwargs)

        if obj:
            self.company = obj
        else:
            self.company = None

        self.company_type_id.choices = self.get_company_type_options()
        self.country.choices = self.get_country_options()

    def get_country_options(self):
        choices = []
        countries = Country.query.order_by('name asc').all()
        for country in countries:
            choices.append((country.iso, country.printable_name))
        return choices

    def get_company_type_options(self):
        choices = []
        types = CompanyType.query.all()
        for t in types:
            choices.append((t.id, t.name))
        return choices

    def save(self):
        if self.company:
            company = self.company
        else:
            company = Company() # this should never happen

        company.company_type_id = self.company_type_id.data
        company.name = self.name.data
        company.address1 = self.address1.data
        company.address2 = self.address2.data
        company.town = self.town.data
        company.city = self.city.data
        company.county = self.county.data
        company.country = self.country.data
        company.post_code = self.post_code.data

        db.session.add(company)
        db.session.commit()

        return company
