"""Invoice view"""

from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, current_app, send_file)
from flask.ext.login import login_required, current_user
from urlparse import urljoin
from datetime import datetime

from nano.models import Invoice, CustomField, InvoiceLink
from nano.forms import InvoiceForm, EmailForm
from nano.extensions import db
from nano.wkhtml import wkhtml_to_pdf
from nano.utils import Struct

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
    custom_fields = CustomField.query.filter_by(user_id=current_user.id).all()

    return render_template('invoice/show.html', invoice=inv, company=company, 
                                                custom_fields=custom_fields)

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
            print 'form saved'
            return redirect(url_for('.show', id=invoice.id))
        else:
            flash('There were errors')
    return render_template('invoice/edit.html', form=form, invoice=invoice)


@invoice.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    invoice = Invoice.query.get(id)
    if invoice:
        db.session.delete(invoice)
        db.session.commit()
        flash('Invoice deleted')
    return redirect(url_for('.index'))

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

@invoice.route('/email/<int:id>', methods=['GET', 'POST'])
def email(id):
    invoice = Invoice.query.get(id)
    if not invoice:
        return 'Invoice not found', 404

    invoice_link = InvoiceLink.query.filter_by(invoice_id=invoice.id).first()
    if not invoice_link:
        invoice_link = InvoiceLink()
        invoice_link.invoice_id = invoice.id
        invoice_link.user_id = invoice.user_id
        invoice_link.generate_link_code()
        db.session.add(invoice_link)
        db.session.commit()

    def render_message(text):
        text = text.replace('{{link}}', invoice_link.get_url())
        text = text.replace('{{company_name}}', current_user.company.name)
        return text

    defaults = {
        'to': invoice.contact.email_address,
        'bcc': current_user.email_address,
        'subject': 'Invoice from %s' % current_user.company.name,
        'message': render_message(current_user.setting.get_val('email_template'))
    }

    form = EmailForm(request.form, Struct(**defaults))

    if request.method == 'post':
        if form.validate():
            form.send_email()
            flash('Email sent')

    return render_template('invoice/email.html', invoice=invoice, invoice_link=invoice_link, form=form)

@invoice.route('/export/<int:id>', methods=['GET'])
@login_required
def export(id):
    invoice = Invoice.query.get(id)
    if not invoice:
        return 'invoice not found', 404
    
    # generate PDF
    # TODO: do this a background job to scale properly
    path = url_for('.pdf', id=invoice.id)
    host = '%s://%s' % (request.scheme, current_app.config['SERVER_NAME'])
    url = urljoin(host, path)
    print url
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
        return 'Invoice not found', 404

    custom_fields = CustomField.query.filter_by(user_id=invoice.user_id).all()
    if not invoice:
        return 'invoice not found', 404
    return render_template('invoice/pdf.html', invoice=invoice, 
                                               company=invoice.user.company,
                                               custom_fields=custom_fields)




