"""Home view"""

import json
import math

from datetime import datetime, timedelta
from collections import OrderedDict
from flask import Blueprint, render_template, redirect, url_for
from flask.ext.login import login_required, current_user
from sqlalchemy import asc

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

    sent_invoices = Invoice.query.filter_by(status='saved') \
                           .filter(Invoice.user_id==current_user.id) \
                           .order_by(asc(Invoice.due_date)) \
                           .all()

    overdue_invoices = Invoice.query.filter_by(status='saved') \
                           .filter(Invoice.payment_status==u'unpaid') \
                           .filter(Invoice.user_id==current_user.id) \
                           .filter(Invoice.due_date<=datetime.now()) \
                           .order_by(asc(Invoice.due_date)) \
                           .all()


    paid_invoices = Invoice.query.filter_by(status='saved') \
                           .filter(Invoice.payment_status==u'paid') \
                           .filter(Invoice.user_id==current_user.id) \
                           .order_by(asc(Invoice.due_date)) \
                           .all()

    draft_invoices      = Invoice.query.filter(Invoice.status=='draft') \
                                       .filter(Invoice.user_id==current_user.id) \
                                       .all()
    payments            = []

    return render_template('home/dashboard.html', user=current_user,
                                                  sent=sent_invoices,
                                                  overdue=overdue_invoices,
                                                  draft_invoices=draft_invoices,
                                                  paid_invoices=paid_invoices,
                                                  payments=payments)

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
                           .filter(Invoice.user_id==current_user.id) \
                           .filter(Invoice.date_issued>=start) \
                           .filter(Invoice.date_issued<=end) \
                           .order_by(asc(Invoice.due_date)) \
                           .all()

    overdue_invoices = Invoice.query.filter_by(status='saved') \
                           .filter(Invoice.payment_status==u'unpaid') \
                           .filter(Invoice.user_id==current_user.id) \
                           .filter(Invoice.date_issued>=start) \
                           .filter(Invoice.date_issued<=end) \
                           .filter(Invoice.due_date<=datetime.now()) \
                           .order_by(asc(Invoice.due_date)) \
                           .all()

    invoice_ids = [invoice.id for invoice in Invoice.query.filter_by(user_id=current_user.id).all()]
    payments = Payment.query.filter(Payment.invoice_id.in_(invoice_ids)) \
                            .order_by(asc(Payment.date)) \
                            .all()

    for invoice in sent_invoices:
        key = invoice.date_issued.strftime(key_format)
        series['sent'][key] += float(invoice.total)

    for invoice in overdue_invoices:
        key = invoice.date_issued.strftime(key_format)
        paid_off = math.fsum([payment.amount for payment in invoice.payments])
        series['overdue'][key] += (float(invoice.total) - paid_off)

    for payment in payments:
        key = payment.date.strftime(key_format)
        series['paid'][key] += float(payment.amount)

    output = [
        {
            'name': 'Billed',
            'data': [v for k, v in series['sent'].iteritems()]
        },
        {
            'name': 'Overdue',
            'data': [v for k, v in series['overdue'].iteritems()]
        },
        {
            'name': 'Paid',
            'data': [v for k, v in series['paid'].iteritems()]
        }
    ]

    data = {
        'series': output,
        'categories': series['sent'].keys()
    }
     
    return json.dumps(data), 200, {'content-type':'application/json'}

