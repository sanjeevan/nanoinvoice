from datetime import datetime
from nano.extensions import db
from nano.utils import get_current_time

class Company(db.Model):
    __tablename__ = 'company'

    id                  = db.Column(u'id', db.BigInteger, primary_key=True, nullable=False)
    user_id             = db.Column(u'user_id', db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    logo_id             = db.Column(u'logo_id', db.BigInteger, db.ForeignKey('file.id'), nullable=False)
    company_type_id     = db.Column(u'type_id', db.BigInteger, db.ForeignKey('type.id'), nullable=False)
    
    name        = db.Column(u'name', db.String(length=255))
    address1    = db.Column(u'address1', db.String(length=255))
    address2    = db.Column(u'address2', db.String(length=255))
    town        = db.Column(u'town', db.String(length=255))
    county      = db.Column(u'county', db.String(length=255))
    country     = db.Column(u'country', db.String(length=3))
    post_code   = db.Column(u'post_code', db.String(length=15))
    
    is_complete         = db.Column(u'is_complete', db.Boolean, default=False)
    last_seen_ip        = db.Column(u'last_seen_ip', db.String(length=40))

    created_at          = db.Column(u'created_at', db.DateTime, nullable=False, default=get_current_time())
    updated_at          = db.Column(u'updated_at', db.DateTime, nullable=False, default=get_current_time())
    
    # user
    user = db.relation('User', primaryjoin='Company.user_id==User.id', backref=db.backref('company', uselist=False))
    
    # logo
    logo = db.relation('File', primaryjoin='Company.logo_id==File.id')
    
    # account type
    company_type = db.relation('CompanyType', backref=db.backref('companies', lazy='dynamic'))
