"""Payment"""

from datetime import datetime
from nano.extensions import db

class Payment(db.Model):
    __tablename__ = 'payment'
    
    id              = db.Column(db.BigInteger, primary_key=True, nullable=False)
    invoice_id      = db.Column(db.BigInteger, db.ForeignKey('invoice.id'))
    date            = db.Column(db.DateTime, default=datetime.now, nullable=False)
    currency_code   = db.Column(db.Unicode(3), nullable=False)
    method          = db.Column(db.Unicode(50), nullable=False)
    description     = db.Column(db.Unicode(255), nullable=True)
    amount          = db.Column(db.Numeric(8, 2), default=0, nullable=False)
    created_at      = db.Column(db.DateTime, default=datetime.now, nullable=False)

    #relation definitions
    invoice             = db.relation('Invoice', 
                                      primaryjoin='Payment.invoice_id==Invoice.id', 
                                      backref=db.backref('payments', lazy='dynamic'))


