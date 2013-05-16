"""This is the client login portal"""

from flask import Blueprint, render_template, redirect, url_for
from flask.ext.login import login_required, current_user

portal = Blueprint('portal', __name__, url_prefix='/portal')

@portal.route('/', methods=['GET'])
def index():
    return render_template('portal/index.html')

@login_required
def view_invoice(id):
    pass

@login_required
def past_invoices():
    pass

@login_required
def signup():
    pass

@login_required
def login():
    pass



