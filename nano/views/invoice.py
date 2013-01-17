from flask import (Flask, Blueprint, render_template, redirect, url_for,
                   flash, request, current_app, send_file)
from flask.ext.login import login_required, current_user
from urlparse import urljoin
from datetime import datetime

from nano.models import Invoice
from nano.forms import InvoiceForm
from nano.utils import json_dumps
from nano.extensions import db
from nano.wkhtml import wkhtml_to_pdf

invoice = Blueprint('invoice', __name__, url_prefix='/invoice')

@invoice.route('/', methods=['GET'])
@login_required
def index():
    invoices = Invoice.query.filter_by(user_id=current_user.id).all()
    return render_template('invoice/index.html', invoices=invoices)

@invoice.route('/<int:id>', methods=['GET'])
@login_required
def show(id):
    inv = Invoice.query.get(id)
    company = inv.user.company
    return render_template('invoice/show.html', invoice=inv, company=company)

@invoice.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = InvoiceForm(request.form)
    if request.method == 'POST':
        if form.validate():
            invoice = form.save()
            return redirect(url_for('.show', id=invoice.id))
        else:
            print form.errors
            flash('There were errors')
    return render_template('invoice/create.html', form=form)


@invoice.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    invoice = Invoice.query.get(id)
    form = InvoiceForm(request.form, obj=invoice)
    if request.method == 'POST':
        if form.validate():
            invoice = form.save()
            return redirect(url_for('.show', id=invoice.id))
        else:
            flash('There were errors')
    return render_template('invoice/edit.html', form=form, invoice=invoice)


@invoice.route('/reopen/<int:id>', methods=['GET', 'POST'])
@login_required
def reopen(id):
    invoice = Invoice.query.get(id)
    if not invoice:
        return 'Invoice not found', 404
    invoice.status = 'draft'
    db.session.add(invoice)
    db.session.commit()
    return redirect(url_for('.show', id=invoice.id))

@invoice.route('/save/<int:id>', methods=['GET', 'POST'])
@login_required
def save(id):
    invoice = Invoice.query.get(id)
    if not invoice:
        return 'Invoice not found', 404
    invoice.status = 'saved'
    db.session.add(invoice)
    db.session.commit()
    return redirect(url_for('.show', id=invoice.id))

@invoice.route('/print')
def print_invoice():
    pass

@invoice.route('/email')
def email():
    pass

@invoice.route('/export/<int:id>', methods=['GET'])
@login_required
def export(id):
    invoice = Invoice.query.get(id)
    if not invoice:
        return 'invoice not found', 404
    
    # generate PDF
    # TODO: do this a background job to scale properly
    path = url_for('.pdf', id=invoice.id)
    url = urljoin(current_app.config['HOSTNAME'], path)
    pdf_path = wkhtml_to_pdf(url)
    if not pdf_path:
        return 'Error generating PDF', 400
    
    # send PDF to browser
    filename = 'invoice-%s-%s.pdf' % (datetime.now().date().isoformat(),
                                      invoice.reference)  
    return send_file(pdf_path, mimetype='application/pdf', as_attachment=True,
                     attachment_filename=filename)

@invoice.route('/pdf/<int:id>', methods=['GET'])
def pdf(id):
    invoice = Invoice.query.get(id)
    if not invoice:
        return 'invoice not found', 404
    return render_template('invoice/pdf.html', invoice=invoice, company=invoice.user.company)
