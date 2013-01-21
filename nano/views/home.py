import json

from datetime import datetime, timedelta
from collections import OrderedDict
from flask import Blueprint, render_template, abort, redirect, url_for, jsonify
from jinja2 import TemplateNotFound
from flask.ext.login import login_required, current_user
from sqlalchemy import asc, desc

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
    """Main dashboard view""" 
    sent_invoices       = Invoice.query.filter_by(status='saved').all()
    draft_invoices      = Invoice.query.filter_by(status='draft').all()
    overdue_invoices    = Invoice.query.filter(Invoice.due_date<=datetime.now()).all()
    payments            = []

    return render_template('home/dashboard.html', user=current_user,
                                                  sent=sent_invoices,
                                                  overdue=overdue_invoices,
                                                  payments=[])

@home.route('/graph')
@login_required
def graph():
    """Returns the JSON data for the graph"""
    series = {
        'sent': OrderedDict(),
        'overdue': OrderedDict(),
        'paid': OrderedDict(),
    }
    
    period = 30 * 6
    start = datetime.now() - timedelta(days=period)
    end = datetime.now() + timedelta(days=period)
    idx = start
    key_format = '%b \'%y'

    while idx <= end:
        key = idx.strftime(key_format)
        series['sent'][key] = 0.0
        series['overdue'][key] = 0.0
        series['paid'][key] = 0.0
        idx = idx + timedelta(days=30)
    
    sent_invoices = Invoice.query.filter_by(status='saved') \
                           .filter(Invoice.date_issued>=start) \
                           .filter(Invoice.date_issued<=end) \
                           .order_by(asc(Invoice.due_date)) \
                           .all()

    overdue_invoices = Invoice.query.filter_by(status='saved') \
                           .filter(Invoice.date_issued>=start) \
                           .filter(Invoice.date_issued<=end) \
                           .filter(Invoice.due_date<=datetime.now()) \
                           .order_by(asc(Invoice.due_date)) \
                           .all()

    for invoice in sent_invoices:
        key = invoice.date_issued.strftime(key_format)
        series['sent'][key] += float(invoice.total)
    
    for invoice in overdue_invoices:
        key = invoice.due_date.strftime(key_format)
        series['overdue'][key] += float(invoice.total)


    output = [
        {
            'name': 'Sent',
            'data': [v for k, v in series['sent'].iteritems()]
        },
        {
            'name': 'Overdue',
            'data': [v for k, v in series['overdue'].iteritems()]
        },
        {
            'name': 'Paid',
            'data': []
        }
    ]

    data = {
        'series': output,
        'categories': series['sent'].keys()
    }
     
    return json.dumps(data), 200, {'content-type':'application/json'}
