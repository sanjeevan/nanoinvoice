"""This is the client login portal

    Requests are routed via a subdomain in the format:
        
        [username].nanoinvoice.com
"""

from flask import Blueprint, render_template, redirect, url_for
from flask.ext.login import login_required, current_user

from nano.models import *

portal = Blueprint('portal', __name__, url_prefix='/portal')

@portal.route('/', methods=['GET'], subdomain='<username>')
def index(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return 'Invalid account', 404
    return render_template('portal/index.html', subdomain=username)

@portal.route('/invoice/<string:paylink>', methods=['GET'], subdomain='<username>')
def invoice(username, paylink):
    user = User.query.filter_by(username=username).first()
    if not user:
        return 'Invalid account', 404

    return render_template('portal/invoice.html')

def login():
    pass



