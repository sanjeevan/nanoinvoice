from werkzeug import (generate_password_hash, check_password_hash,
                      cached_property)

from nano.extensions import db
from nano.utils import get_current_time, VARCHAR_LEN_128

class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    thumbnail_id = db.Column(db.Integer, db.ForeignKey('file.id'))
    full_image_id = db.Column(db.Integer, db.ForeignKey('file.id'))

    slug = db.Column(db.String(255))
    title = db.Column(db.String(255))
    summary = db.Column(db.String)
    summary_html = db.Column(db.String)
    body = db.Column(db.String)
    body_html = db.Column(db.String)
    
    total_comments = db.Column(db.Integer(3), default=0)
    
    # ratings
    rating_enabled = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer, default=0)
    
    # publish
    published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime, default=get_current_time())
    
    # times
    created_at = db.Column(db.DateTime, default=get_current_time())
    updated_at = db.Column(db.DateTime, default=get_current_time())

    @classmethod
    def get_featured(cls, limit=5):
        pass
