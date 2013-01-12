from datetime import datetime
from nano.extensions import db
from nano.utils import get_current_time

class Logo(db.Model):
    __tablename__ = 'logo'

    id                  = db.Column(u'id', db.BigInteger, primary_key=True, nullable=False)
    original_image_id   = db.Column(u'original_image_id', db.BigInteger, db.ForeignKey('file.id'), nullable=False)
    thumbnail_image_id  = db.Column(u'thumbnail_image_id', db.BigInteger, db.ForeignKey('file.id'), nullable=False)
   
    original = db.relation('File', primaryjoin='Logo.original_image_id==File.id', 
                                   backref=db.backref('original', uselist=False))

    thumbnail = db.relation('File', primaryjoin='Logo.thumbnail_image_id==File.id', 
                                    backref=db.backref('thumbnail', uselist=False)) 
