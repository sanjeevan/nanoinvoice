"""This is the client login portal"""

from flask import Flask, Blueprint, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound
from flask.ext.login import login_required, current_user

portal = Blueprint('portal', __name__, url_prefix='/portal')

@payment.route('/', methods=['GET'])
def index():
    return render_template('portal/index.html')

def view_invoice(id):
    pass

def past_invoices():
    pass

def signup():
    pass

def login():
    pass



