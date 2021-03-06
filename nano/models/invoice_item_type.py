from datetime import datetime
from nano.extensions import db
from nano.utils import get_current_time, model_to_dict

class InvoiceItemType(db.Model):
    __tablename__ = 'invoice_item_type'

    #column definitions
    id          = db.Column(u'id', db.Integer, primary_key=True, nullable=False)
    name        = db.Column(u'name', db.String(length=20))
    name_plural = db.Column(u'name_plural', db.String(length=20))
    sort_order  = db.Column(u'sort_order', db.Integer)
    updated_at  = db.Column(u'updated_at', db.DateTime, nullable=False)
    created_at  = db.Column(u'created_at', db.DateTime, nullable=False)
    
    def name_pluralized(self, quantity):
        if quantity > 1:
            return self.name_plural
        else:
            return self.name

    def serialize(self):
        return model_to_dict(self)

