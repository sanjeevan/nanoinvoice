from datetime import datetime
from nano.extensions import db
from nano.utils import get_current_time

class Company(db.Model):
    __tablename__ = 'company'

    id                  = db.Column(u'id', db.BigInteger, primary_key=True, nullable=False)
    user_id             = db.Column(u'user_id', db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    logo_id             = db.Column(u'logo_id', db.BigInteger, db.ForeignKey('logo.id'), nullable=False)
    company_type_id     = db.Column(u'company_type_id', db.BigInteger, db.ForeignKey('company_type.id'), nullable=False)
    
    name        = db.Column(u'name', db.Unicode(length=255))
    address1    = db.Column(u'address1', db.Unicode(length=255))
    address2    = db.Column(u'address2', db.Unicode(length=255))
    town        = db.Column(u'town', db.Unicode(length=100))
    city        = db.Column(u'city', db.Unicode(length=100))
    county      = db.Column(u'county', db.Unicode(length=255))
    country     = db.Column(u'country', db.Unicode(length=2))
    post_code   = db.Column(u'post_code', db.Unicode(length=20))
    registration_number = db.Column(u'registration_number', db.Unicode(length=20))
    
    created_at          = db.Column(u'created_at', db.DateTime, nullable=False, default=get_current_time())
    updated_at          = db.Column(u'updated_at', db.DateTime, nullable=False, default=get_current_time())
    
    # user
    user = db.relation('User', primaryjoin='Company.user_id==User.id', backref=db.backref('company', uselist=False))
    
    # logo
    logo = db.relation('Logo', primaryjoin='Company.logo_id==Logo.id')
    
    # account type
    company_type = db.relation('CompanyType', backref=db.backref('companies', lazy='dynamic'))
