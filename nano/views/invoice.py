from flask import (Flask, Blueprint, render_template, abort, redirect, url_for,
                   flash, request)
from jinja2 import TemplateNotFound
from flask.ext.login import login_required, current_user

from nano.models import Invoice
from nano.forms import InvoiceForm
from nano.utils import json_dumps

invoice = Blueprint('invoice', __name__, url_prefix='/invoice')

@invoice.route('/', methods=['GET'])
@login_required
def index():
    invoices = Invoice.query.filter_by(user_id=current_user.id).all()
    return render_template('invoice/index.html', invoices=invoices)

@invoice.route('/<int:id>', methods=['GET'])
def show(id):
    inv = Invoice.query.get(id)
    profile = inv.user.profile
    print json_dumps(inv.serialize())
    return render_template('invoice/show.html', invoice=inv, profile=profile)

@invoice.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = InvoiceForm(request.form)
    
    if request.method == 'POST':
        if form.validate():
            invoice = form.save()
            return redirect(url_for('.show', id=invoice.id))
        else:
            flash('There were errors')

    return render_template('invoice/create.html', form=form)
