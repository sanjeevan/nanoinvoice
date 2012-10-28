from datetime import datetime
from nano.extensions import db
from nano.utils import get_current_time

class Currency(db.Model):
    __tablename__ = 'currency'

    #column definitions
    id = db.Column(u'id', db.BigInteger, primary_key=True, nullable=False)
    code = db.Column(u'code', db.String(length=6))
    name = db.Column(u'name', db.String(length=50))
    symbol = db.Column(u'symbol', db.String(length=6))
    
    updated_at = db.Column(u'updated_at', db.DateTime(), nullable=False)
    created_at = db.Column(u'created_at', db.DateTime(), nullable=False)

 
