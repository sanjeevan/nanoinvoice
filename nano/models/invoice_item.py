import math

from datetime import datetime
from nano.extensions import db
from nano.utils import get_current_time

class InvoiceItem(db.Model):
    __tablename__ = 'invoice_item'
    
    id              = db.Column(u'id', db.BigInteger, primary_key=True, nullable=False)
    invoice_id      = db.Column(u'invoice_id', db.BigInteger, db.ForeignKey('invoice.id')) 
    type_id         = db.Column(u'type_id', db.BigInteger, db.ForeignKey('invoice_item_type.id')) 
    tax_rate_id     = db.Column(u'tax_rate_id', db.BigInteger, db.ForeignKey('tax_rate.id')) 

    description     = db.Column(u'description', db.String)

    quantity        = db.Column(u'quantity', db.Numeric(8, 2))
    price           = db.Column(u'price', db.Numeric(8, 2))
    tax             = db.Column(u'tax', db.Numeric(8, 2))
    total           = db.Column(u'total', db.Numeric(8, 2))

    sort_order      = db.Column(u'sort_order', db.Integer, default=0)

    #relation definitions
    invoice_item_type   = db.relation('InvoiceItemType', primaryjoin='InvoiceItem.type_id==InvoiceItemType.id')
    invoice             = db.relation('Invoice', primaryjoin='InvoiceItem.invoice_id==Invoice.id', backref='invoice_items')
    tax_rate            = db.relation('TaxRate', primaryjoin='InvoiceItem.tax_rate_id==TaxRate.id')

    def should_render_field(self, name):
        no_render = {'Comment': ['quantity', 'price', 'tax', 'total'],
                     'VAT': ['quantity'] }

        type_name = self.invoice_item_type.name
        if not type_name in no_render:
            return True
        
        if name in no_render[type_name]:
            return False

        return True


    def quantity_str(self):
        if self.invoice_item_type.name == 'Hours':
            mins = self.quantity * 60
            hours = 0
            while mins >= 60:
                mins -= 60
                hours += 1
            if mins == 0:
                return hours
            else:
                mins = round(mins)
                mins = str(mins).zfill(2)
                return '%s:%s' % (hours, mins)
        return int(self.quantity) if math.fmod(self.quantity, 1) == 0 else self.quantity
