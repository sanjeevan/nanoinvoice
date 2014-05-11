import os
import uuid
import hashlib
import shutil
import mimetypes

from datetime import datetime
from flask import current_app, url_for
from werkzeug import secure_filename

from nano.extensions import db
from nano.utils import get_current_time

class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(db.String(255))
    filesize = db.Column(db.Integer)
    extension = db.Column(db.String(25))
    mimetype = db.Column(db.String(255))
    location = db.Column(db.String(255))

    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    hash = db.Column(db.String(40))

    # times
    created_at = db.Column(db.DateTime, default=get_current_time())
    updated_at = db.Column(db.DateTime, default=get_current_time())

    def is_image(self):
        extensions = ['jpg', 'jpeg', 'png', 'bmp', 'gif']
        if self.extension in extensions:
            return True
        return False

    def get_web_url(self, w=80, h=80, method='normal'):
        return self.location.replace(current_app.config['UPLOAD_DIR'] + '/', '')

    @classmethod
    def save_uploaded_file(cls, fs, filename=None):
        # make a new folder for the image
        now = datetime.now()
        _uuid = uuid.uuid4().hex
        path = '%s/%s/%s/%s/%s/%s' % (now.year, now.month, now.day, _uuid[:3],
                                      _uuid[3:6], _uuid[6:])
        base_path = os.path.join(current_app.config['UPLOAD_DIR'], path)
        os.makedirs(base_path)

        name = secure_filename(fs.filename) if filename is None else filename
        save_path = os.path.join(base_path, name)
        fs.save(save_path)

        # get hash of file contents
        f1 = open(save_path, 'rb')
        sha1sum = hashlib.sha1(f1.read()).hexdigest()
        f1.close()

        obj = File()
        obj.filename    = fs.filename
        obj.filesize    = os.path.getsize(save_path)
        obj.mimetype    = fs.mimetype
        obj.extension   = fs.filename.rsplit('.', 1)[1]
        obj.location    = save_path
        obj.hash        = sha1sum
        return obj

    @classmethod
    def create_from_file(cls, oldpath, filename=None):
        now = datetime.now()
        _uuid = uuid.uuid4().hex
        path = '%s/%s/%s/%s/%s/%s' % (now.year, now.month, now.day, _uuid[:3],
                                      _uuid[3:6], _uuid[6:])
        base_path = os.path.join(current_app.config['UPLOAD_DIR'], path)
        os.makedirs(base_path)

        save_path = os.path.join(base_path, filename)
        shutil.copy(oldpath, save_path)

        # get hash of file contents
        f1 = open(save_path, 'rb')
        sha1sum = hashlib.sha1(f1.read()).hexdigest()
        f1.close()

        obj = File()
        obj.filename    = filename
        obj.filesize    = os.path.getsize(save_path)
        obj.mimetype    = mimetypes.guess_type(oldpath)[0]
        obj.extension   = filename.rsplit('.', 1)[1]
        obj.location    = save_path
        obj.hash        = sha1sum
        return obj


