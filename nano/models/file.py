import os

from datetime import datetime
from flask import current_app, url_for
from werkzeug import (generate_password_hash, check_password_hash,
                      cached_property)

from nano.extensions import db
from nano.utils import get_current_time, VARCHAR_LEN_128

class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(db.String(255))
    filesize = db.Column(db.Integer(20))
    extension = db.Column(db.String(25))
    mimetype = db.Column(db.String(255))
    location = db.Column(db.String(255))
    
    meta_width = db.Column(db.Integer(11))
    meta_height = db.Column(db.Integer(11))
    hash = db.Column(db.String(32))
    source = db.Column(db.String(20))
    
    # times
    created_at = db.Column(db.DateTime, default=get_current_time())
    updated_at = db.Column(db.DateTime, default=get_current_time())

    def is_image(self):
        extensions = ['jpg', 'jpeg', 'png', 'bmp', 'gif']
        if self.extension in extensions:
            return True
        return False

    def get_formatted_filesize(self):
        pass

    def get_thumbnail_filename(self, w=80, h=80, method='normal'):
        base_path = os.path.join(current_app.config['UPLOAD_DIR'], 'thumbnails')
        dt = self.created_at
        f1 = '%s/%s/%s' % (dt.year, dt.month, dt.day)
        f2 = '%s/%s/%s' % (self.hash[:3], self.hash[3:6], self.hash[6:9])
        f3 = '%s' % self.hash[9:]
        filename = '%s/%s/%s/%s-%s-px-%s-thumb.png' % (f1, f2, f3, w, h, method)
        return os.path.join(base_path, filename)

    def get_thumbnail_url(self, w=80, h=80, method='normal'):
        filename = self.get_thumbnail_filename(w, h, method)
        if os.path.isfile(filename) or True:
            return filename.replace(current_app.config['UPLOAD_DIR'], '/uploads')
        else:
            return url_for('file.thumbnail', id=self.id, w=w, h=h, method=method)

