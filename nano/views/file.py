from flask import (Blueprint, render_template, request, flash, url_for,
                   send_from_directory, current_app)
from flask.ext.login import current_user
from flask import current_app
from PIL import Image

from nano.models import File, Company
from nano.extensions import db

file = Blueprint("file", __name__, url_prefix='/file')

def allowed_file(name):
    """Returns True if the filename has an image type extension"""
    valid_extensions = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in name and name.rsplit('.', 1)[1] in valid_extensions 

@file.route('/download/<path:location>', methods=['GET'])
def download(location):
    print location
    return send_from_directory(current_app.config['UPLOAD_DIR'], location)

@file.route('/photo_upload', methods=['POST'])
def photo_upload():
    file_upload = request.files['Filedata']
    if not file_upload:
        return 'No file uploaded', 400
    if not allowed_file(file_upload.filename):
        return 'Extension not allowed', 400
    else:
        f = File.save_uploaded_file(file_upload)
        file_upload.close()

        # save to database
        db.session.add(f)
        db.session.commit()

        company = Company.query.filter_by(user_id=current_user.id).first()
        company.logo_id = f.id
        db.session.add(company)
        db.session.commit()
        
        # resize down to a sane size
        fp = open(f.location)
        image = Image.open(fp)
        image.thumbnail((280, 280), Image.ANTIALIAS)
        image.save(f.location)
        fp.close()

        return 'ok', 200
