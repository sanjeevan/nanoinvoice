from flask import Flask, Blueprint, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound
from flask.ext.login import login_required, current_user

invoice = Blueprint('invoice', __name__, url_prefix='/invoice')

@invoice.route('/', methods=['GET'])
@login_required
def index():
    return render_template('invoice/index.html')
