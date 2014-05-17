from datetime import datetime
from nano.extensions import db

class WebhookLog(db.Model):
    __tablename__ = 'webhook_log'

    id          = db.Column(db.BigInteger, primary_key=True, nullable=False)
    service     = db.Column(db.Unicode(100))
    data        = db.Column(db.UnicodeText)
    ip          = db.Column(db.Unicode(50))
    headers     = db.Column(db.UnicodeText)
    created_at  = db.Column(db.DateTime, nullable=False, default=datetime.now)
