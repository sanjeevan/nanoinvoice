from datetime import datetime
from nano.extensions import db
from nano.utils import get_current_time

class PaymentTerm(db.Model):
    __tablename__ = 'payment_term'

    #column definitions
    id = db.Column(u'id', db.BigInteger, primary_key=True, nullable=False)
    days = db.Column(u'days', db.Integer)
    name = db.Column(u'name', db.String(length=50))
    updated_at = db.Column(u'updated_at', db.DateTime, nullable=False)
    created_at = db.Column(u'created_at', db.DateTime, nullable=False) 
