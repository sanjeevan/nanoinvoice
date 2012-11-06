from datetime import datetime
from nano.extensions import db
from nano.utils import get_current_time

class Contact(db.Model):
    __tablename__ = 'contact'

    #column definitions
    id = db.Column(u'id', db.BigInteger, primary_key=True, nullable=False)
    user_id = db.Column(u'user_id', db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    email_address = db.Column(u'email_address', db.String(length=255))
    first_name = db.Column(u'first_name', db.String(length=255))
    last_name = db.Column(u'last_name', db.String(length=255))
    organisation = db.Column(u'organisation', db.String(length=255))
    
    address_country_code = db.Column(u'address_country_code', db.String(length=4))
    address_county = db.Column(u'address_county', db.String(length=255))
    address_line1 = db.Column(u'address_line1', db.String(length=255))
    address_line2 = db.Column(u'address_line2', db.String(length=255))
    address_line3 = db.Column(u'address_line3', db.String(length=255))
    address_post_code = db.Column(u'address_post_code', db.String(length=15))
    address_town = db.Column(u'address_town', db.String(length=255))
    billing_email_address = db.Column(u'billing_email_address', db.String(length=255))

    created_at = db.Column(u'created_at', db.DateTime, nullable=False,
                           default=get_current_time())
    updated_at = db.Column(u'updated_at', db.DateTime, nullable=False,
                           default=get_current_time())

    #relation definitions
    user = db.relation('User', primaryjoin='Contact.user_id==User.id')
