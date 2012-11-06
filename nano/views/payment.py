from flask import Flask, Blueprint, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound
from flask.ext.login import login_required, current_user

payment = Blueprint('payment', __name__, url_prefix='/payment')

@payment.route('/', methods=['GET'])
@login_required
def index():
    return render_template('payment/index.html')
