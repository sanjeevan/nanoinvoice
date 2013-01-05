from datetime import datetime
from nano.extensions import db
from nano.utils import get_current_time

class Contact(db.Model):
    __tablename__ = 'contact'

    #column definitions
    id              = db.Column(u'id', db.BigInteger, primary_key=True, nullable=False)
    user_id         = db.Column(u'user_id', db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    first_name      = db.Column(u'first_name', db.String(length=255))
    last_name       = db.Column(u'last_name', db.String(length=255))
    organisation    = db.Column(u'organisation', db.String(length=255))
    email_address   = db.Column(u'email_address', db.String(length=255))
    billing_email_address = db.Column(u'billing_email_address', db.String(length=255))
    
    address_line1   = db.Column(u'address_line1', db.String(length=255))
    address_line2   = db.Column(u'address_line2', db.String(length=255))
    town            = db.Column(u'town', db.String(length=255))
    city            = db.Column(u'city', db.String(length=255))
    county          = db.Column(u'county', db.String(length=255))
    country         = db.Column(u'country', db.String(length=2))
    post_code       = db.Column(u'post_code', db.String(length=15))

    created_at      = db.Column(u'created_at', db.DateTime, nullable=False,
                                default=get_current_time())
    updated_at      = db.Column(u'updated_at', db.DateTime, nullable=False,
                                default=get_current_time())

    #relation definitions
    user = db.relation('User', primaryjoin='Contact.user_id==User.id', backref='contacts')

    def full_name(self):
        return self.first_name + ' ' + self.last_name
