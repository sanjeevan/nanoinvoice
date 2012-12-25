from flask import (Flask, Blueprint, render_template, abort, redirect, url_for,
                   flash, request, Response)
from jinja2 import TemplateNotFound
from flask.ext.login import login_required, current_user

from nano.models import Invoice, InvoiceItem
from nano.forms import InvoiceForm, InvoiceItemForm
from nano.utils import json_dumps 
from nano.extensions import db

invoice_item = Blueprint('invoice_item', __name__, url_prefix='/invoice_item')

@invoice_item.route('/', methods=['GET'])
@login_required
def index():
    invoices = Invoice.query.filter_by(user_id=current_user.id).all()
    return render_template('invoice/index.html', invoices=invoices)

@invoice_item.route('/create', methods=['POST'])
def create():
    form = InvoiceItemForm(request.form)

    if form.validate():
        invoice_item = form.save()
        ret = {'Invoice': invoice_item.invoice.serialize(), 'InvoiceItem':
                invoice_item.serialize() }
        return Response(json_dumps(ret), content_type='application/json')
    else:
        return 'There was an error', 400 
    

@invoice_item.route('/update/<int:id>', methods=['POST'])
def update(id):
    invoice_item = InvoiceItem.query.get(id)
    form = InvoiceItemForm(request.form, obj=invoice_item)

    if form.validate():
        invoice_item = form.save()
        ret = {'Invoice': invoice_item.invoice.serialize(), 'InvoiceItem':
                invoice_item.serialize() }
        return Response(json_dumps(ret), content_type='application/json')
    else:
        return 'There was an error', 400 

@invoice_item.route('/delete', methods=['DELETE'])
def delete():
    invoice_item = InvoiceItem.query.get(request.args.get('id'))
    if not invoice_item:
        return 'Not found', 404
    else:
        db.session.delete(invoice_item)
        db.session.commit()
        return 'Deleted', 200
