from datetime import datetime
from nano.extensions import db
from nano.utils import get_current_time

class TaxRate(db.Model):
    __tablename__ = 'tax_rate'

    id = db.Column(u'id', db.BigInteger, primary_key=True, nullable=False)
    user_id = db.Column(u'user_id', db.BigInteger, db.ForeignKey('user.id'))

    type = db.Column(u'type', db.String(255))
    name = db.Column(u'name', db.String(255))
    rate = db.Column(u'rate', db.Numeric(8, 2), nullable=True)

    updated_at = db.Column(u'updated_at', db.DateTime(), nullable=False, default=get_current_time())
    created_at = db.Column(u'created_at', db.DateTime(), nullable=False, default=get_current_time())

    user = db.relation('User', lazy='select', backref='tax_rates')  
