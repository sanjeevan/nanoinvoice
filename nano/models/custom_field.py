from datetime import datetime
from nano.extensions import db
from nano.utils import get_current_time

class CustomField(db.Model):
    __tablename__ = 'custom_field'

    id          = db.Column(u'id', db.BigInteger, primary_key=True, nullable=False)
    user_id     = db.Column(u'user_id', db.Integer, db.ForeignKey('user.id'), nullable=False)
    invoice_id  = db.Column(u'invoice_id', db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    
    name        = db.Column(u'name', db.Unicode(length=255))
    value       = db.Column(u'value', db.Unicode(length=255))

    # user
    user        = db.relation('User', backref=db.backref('custom_fields'))
    invoice     = db.relation('Invoice', backref=db.backref('custom_fields'))
