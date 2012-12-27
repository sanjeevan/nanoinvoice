from flask import Flask, Blueprint, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound
from flask.ext.login import login_required, current_user

from nano.models import InvoiceItemType, TaxRate 

js = Blueprint('app_js', __name__, url_prefix='/app_js')

@js.route('/constants.js', methods=['GET'])
def constants():
    tax_rates = []
    if current_user.is_authenticated():
        tax_rates = TaxRate.query.filter_by(user_id=current_user.id).all()
    else:
        tax_rates = []

    invoice_item_types = InvoiceItemType.query.all() 
    return render_template('js/constants.html', tax_rates=tax_rates,
                           item_types=invoice_item_types)
