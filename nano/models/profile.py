from datetime import datetime
from nano.extensions import db
from nano.utils import get_current_time

class Profile(db.Model):
    __tablename__ = 'profile'

    id                  = db.Column(u'id', db.BigInteger, primary_key=True, nullable=False)
    user_id             = db.Column(u'user_id', db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    logo_id             = db.Column(u'logo_id', db.BigInteger, db.ForeignKey('file.id'), nullable=False)
    company_type_id     = db.Column(u'company_type_id', db.BigInteger, db.ForeignKey('account_type.id'), nullable=False)
    
    company_name        = db.Column(u'company_name', db.String(length=255))
    company_address1    = db.Column(u'company_address1', db.String(length=255))
    company_address2    = db.Column(u'company_address2', db.String(length=255))
    company_town        = db.Column(u'company_town', db.String(length=255))
    company_county      = db.Column(u'company_county', db.String(length=255))
    company_post_code   = db.Column(u'company_post_code', db.String(length=15))
    
    is_complete         = db.Column(u'is_complete', db.Boolean, default=False)
    last_seen_ip        = db.Column(u'last_seen_ip', db.String(length=40))

    created_at          = db.Column(u'created_at', db.DateTime, nullable=False, default=get_current_time())
    updated_at          = db.Column(u'updated_at', db.DateTime, nullable=False, default=get_current_time())
    
    # user
    user = db.relation('User', primaryjoin='Profile.user_id==User.id', backref=db.backref('profile', uselist=False))
    
    # logo
    logo = db.relation('File', primaryjoin='Profile.logo_id==File.id')
    
    # account type
    # TODO: rename field to account_type_id
    company_type = db.relation('AccountType', backref=db.backref('profiles', lazy='dynamic'))
