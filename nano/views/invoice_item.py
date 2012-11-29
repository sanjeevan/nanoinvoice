from flask import (Flask, Blueprint, render_template, abort, redirect, url_for,
                   flash, request)
from jinja2 import TemplateNotFound
from flask.ext.login import login_required, current_user

from nano.models import Invoice
from nano.forms import InvoiceForm

invoice_item = Blueprint('invoice_item', __name__, url_prefix='/invoice_item')

@invoice_item.route('/', methods=['GET'])
@login_required
def index():
    invoices = Invoice.query.filter_by(user_id=current_user.id).all()
    return render_template('invoice/index.html', invoices=invoices)


@invoice_item.route('/edit', methods=['GET'])
def edit(id):
    pass

@invoice_item.route('/delete', methods=['GET'])
def delete(id):
    pass
