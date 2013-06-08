"""File view"""

import tempfile
import os

from flask import (Blueprint, render_template, request, flash, url_for,
                   send_from_directory, current_app, jsonify)
from flask.ext.login import current_user
from flask import current_app
from PIL import Image

from nano.models import File, Company, Logo
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

        # store original image
        original = File.save_uploaded_file(file_upload)
        file_upload.close()
 
        # create a thumbnailed version
        temp_fd, temp_path = tempfile.mkstemp('.jpg', 'thumbnail')
        image_fp = open(original.location)
        image = Image.open(image_fp)
        image.thumbnail((300, 300), Image.ANTIALIAS)
        image.save(temp_path, 'JPEG', quality=100)
        image_fp.close()
        os.close(temp_fd) # close fd
        
        # store thumbnailed version
        thumbnail = File.create_from_file(temp_path, 'logo.jpg')
        os.unlink(temp_path)
        
        # save to db
        db.session.add(original)
        db.session.add(thumbnail)
        db.session.commit() 
        
        # delete old photo if it exists 
        company = Company.query.filter_by(user_id=current_user.id).first()
        if company.logo:
            db.session.delete(company.logo)
            db.session.commit()
        
        # create new logo entry
        logo = Logo()
        logo.original_image_id = original.id
        logo.thumbnail_image_id = thumbnail.id
        db.session.add(logo)
        db.session.commit()
        
        # update company 
        company.logo_id = logo.id
        db.session.add(company)
        db.session.commit()
        
        url1 = url_for('file.download', location=company.logo.thumbnail.get_web_url())
        resp = '<img src="%s">' % url1
        return resp

