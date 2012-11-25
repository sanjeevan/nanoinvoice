from flask import (Flask, Blueprint, render_template, abort, redirect, url_for,
                   flash, request)
from jinja2 import TemplateNotFound
from flask.ext.login import login_required, current_user

from nano.models import Invoice
from nano.forms import InvoiceForm

invoice = Blueprint('invoice', __name__, url_prefix='/invoice')

@invoice.route('/', methods=['GET'])
@login_required
def index():
    invoices = Invoice.query.filter_by(user_id=current_user.id).all()
    return render_template('invoice/index.html', invoices=invoices)

@invoice.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = InvoiceForm(request.form)
    
    if request.method == 'POST':
        if form.validate():
            form.save()
        else:
            print form.errors
            flash('There were errors')

    return render_template('invoice/create.html', form=form)
