"""Invoice link"""

from flask import current_app
from datetime import datetime

from nano.extensions import db
from nano.utils import encode_id 

class InvoiceLink(db.Model):
    __tablename__ = 'invoice_link'

    #column definitions
    id          = db.Column(db.Integer(11), primary_key=True, nullable=False)
    user_id     = db.Column(db.Integer(11), db.ForeignKey('user.id'), nullable=False)
    invoice_id  = db.Column(db.Integer(11), db.ForeignKey('invoice.id'), nullable=False)
    link        = db.Column(db.Unicode(25), default=u'', nullable=False)

    def generate_link_code(self):
        code = str(self.user_id) + str(self.invoice_id)
        self.link = encode_id(int(code))
        return self.link

    def get_url(self):
        url = 'http://%s.%s/portal/invoice/%s' % (self.user.username,
                                                  current_app.config['SERVER_NAME'],
                                                  self.link)
        return url

