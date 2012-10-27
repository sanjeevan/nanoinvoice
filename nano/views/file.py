from flask import Flask, Blueprint, render_template, abort
from jinja2 import TemplateNotFound

file = Blueprint("file", __name__, url_prefix='/file')

@file.route('/thumbnail/<int:id>', methods=["GET"])
def thumbnail():
    return 'thumbnail'

@file.route('/download/<int:id>', methods=['GET'])
def download(id):
    return 'download'
