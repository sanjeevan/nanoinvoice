from datetime import datetime
from nano.extensions import db
from nano.utils import get_current_time, model_to_dict, json_dumps

class Invoice(db.Model):
    __tablename__ = 'invoice'

    id                  = db.Column(u'id', db.BigInteger, primary_key=True, nullable=False)
    user_id             = db.Column(u'user_id', db.BigInteger, db.ForeignKey('user.id')) 
    contact_id          = db.Column(u'contact_id', db.BigInteger, db.ForeignKey('contact.id')) 
    payment_term_id     = db.Column(u'payment_term_id', db.BigInteger, db.ForeignKey('payment_term.id')) 
    status              = db.Column(u'status', db.String(255))
    reference           = db.Column(u'reference', db.String(255))
    po_reference        = db.Column(u'po_reference', db.String(255))
    currency_code       = db.Column(u'currency_code', db.String(5))
    date_issued         = db.Column(u'date_issued', db.DateTime)
    due_date            = db.Column(u'due_date', db.DateTime)
    written_off_date    = db.Column(u'written_off_date', db.DateTime)
    sub_total           = db.Column(u'sub_total', db.Numeric(8, 2))
    tax                 = db.Column(u'tax', db.Numeric(8, 2))
    total               = db.Column(u'total', db.Numeric(8, 2))

    updated_at          = db.Column(u'updated_at', db.DateTime, nullable=False, default=get_current_time())
    created_at          = db.Column(u'created_at', db.DateTime, nullable=False, default=get_current_time())

    # relations
    user                = db.relation('User', primaryjoin='Invoice.user_id==User.id', backref='invoices')
    contact             = db.relation('Contact', primaryjoin='Invoice.contact_id==Contact.id')
    payment_term        = db.relation('PaymentTerm', primaryjoin='Invoice.payment_term_id==PaymentTerm.id')
    
    @classmethod
    def next_invoice_number(cls, user):
        """Next the next invoice number for the user"""
        cur_max = cls.query.filter_by(user_id=user.id).count()
        cur_max += 1

        return str(cur_max)

    def next_item_sort_order(self):
        """Generate the next number for the invoice item's sort order"""
        from nano.models import InvoiceItem
        total = InvoiceItem.query.filter_by(invoice_id=self.id).count()
        return total+1
    
    def update_totals(self):
        """Update total and tax"""
        sub_total = 0
        tax = 0
        for item in self.invoice_items:
            sub_total += item.total
            tax += item.tax

        self.tax = tax
        self.sub_total = sub_total
        self.total = self.tax + self.sub_total
        return True
    
    def serialize(self):
        d = model_to_dict(self)
        d['InvoiceItems'] = [item.serialize() for item in self.invoice_items] 
        return d

    def __json__(self):
        return json_dumps(self.serialize())


