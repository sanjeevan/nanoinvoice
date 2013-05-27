"""Payment"""

from datetime import datetime
from nano.extensions import db

class Payment(db.Model):
    __tablename__ = 'payment'
    
    id              = db.Column(u'id', db.BigInteger, primary_key=True, nullable=False)
    invoice_id      = db.Column(u'invoice_id', db.BigInteger, db.ForeignKey('invoice.id'))
    date            = db.Column(u'date', db.DateTime, default=datetime.now)
    currency_code   = db.Column(u'currency_code', db.Unicode(3), nullable=False)
    method          = db.Column(u'method', db.Unicode(50))
    amount          = db.Column(u'amount', db.Numeric(8, 2))
    created_at      = db.Column(u'created_at', db.DateTime, default=datetime.now)

    #relation definitions
    invoice             = db.relation('Invoice', 
                                      primaryjoin='Payment.invoice_id==Invoice.id', 
                                      backref=db.backref('payments', lazy='dyanmic'))


