
from datetime import datetime
from flask import Flask, Blueprint, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound
from flask.ext.login import login_required, current_user

from nano.models import *

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated():
        return redirect('/dashboard')

    return render_template('home/index.html')

@home.route('/login')
def login():
    return redirect(url_for('account.login'))

@home.route('/dashboard')
@login_required
def dashboard():
    
    sent_invoices       = Invoice.query.filter_by(status='saved').all()
    draft_invoices      = Invoice.query.filter_by(status='draft').all()
    overdue_invoices    = Invoice.query.filter(Invoice.due_date<=datetime.now()).all()

    return render_template('home/dashboard.html', user=current_user,
                                                  sent=sent_invoices,
                                                  overdue=overdue_invoices)
