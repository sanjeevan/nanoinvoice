# -*- coding: utf-8 -*-

from flask import (Blueprint, render_template, request,
                   flash, url_for, redirect)
from flask.ext.login import current_user, login_required

from nano.models import (CustomField, TaxRate,
                         GoCardlessAccount, StripeAccount)
from nano.extensions import db
from nano.forms import (CustomFieldsManagementForm,
                        TaxRateContainerForm, SettingForm,
                        PaymentIntegrationForm)
from nano.utils import Struct

settings = Blueprint('settings', __name__, url_prefix='/settings')

@settings.route('/', methods=['GET', 'POST'])
def index():
    defaults = {
        'email_template': current_user.setting.get_val('email_template', '')
    }

    form = SettingForm(request.form, obj=Struct(**defaults))
    if request.method == 'POST':
        if form.validate():
            form.save(current_user)
            flash('Settings updated')
        else:
            flash('There were errors')
    
    return render_template('settings/index.html', form=form)

# -- Custom fields

@settings.route('/custom_fields', methods=['GET', 'POST'])
@login_required
def custom_fields():
    """Application settings"""
    custom_fields = CustomField.query.filter_by(user_id=current_user.id).all() 

    data = CustomFieldsManagementForm.transform(custom_fields)
    form = CustomFieldsManagementForm(request.form, obj=data)

    if request.method == 'POST' and form.validate():
        form.save()
        flash('New custom field added')
        return redirect(request.referrer)
    else:
        print form.errors

    return render_template('settings/custom_fields.html', form=form,
                                                          custom_fields=custom_fields)

@settings.route('/custom_fields/delete/<int:id>', methods=['GET'])
@login_required
def delete_custom_field(id):
    custom_field = CustomField.query.get(id)
    if custom_field:
        db.session.delete(custom_field)
        db.session.commit()
        flash('Custom field deleted')
    return redirect(request.referrer)


# -- Tax rates

@settings.route('/tax_rates', methods=['GET', 'POST'])
@login_required
def tax_rates():
    tax_rates = TaxRate.query.filter(TaxRate.user_id==current_user.id).all()
    
    data = TaxRateContainerForm.to_form_data(tax_rates)
    form = TaxRateContainerForm(request.form, obj=data)

    if request.method == 'POST' and form.validate():
        tax_rate = form.save()
        if tax_rate:
            flash('New tax rate added')
        else:
            flash('Tax rates updated')
        return redirect(request.referrer)
    else:
        print form.errors

    return render_template('settings/tax_rates.html', tax_rates=tax_rates, 
                                                      form=form)

@settings.route('/tax_rates/delete/<int:id>', methods=['GET'])
@login_required
def delete_tax_rate(id):
    tax_rate = TaxRate.query.get(id)
    if tax_rate:
        db.session.delete(tax_rate)
        db.session.commit()
        flash('Tax rate deleted')
    return redirect(request.referrer)


@settings.route('/payment_integration', methods=['GET', 'POST'])
@login_required
def payment_integration():
    
    gocardless_account = GoCardlessAccount.get_or_create_for_user(current_user.id)
    stripe_account = StripeAccount.get_or_create_for_user(current_user.id)

    data = Struct(**{
        'gocardless': gocardless_account,
        'stripe': stripe_account
    })

    form = PaymentIntegrationForm(request.form, obj=data)

    if request.method == 'POST':
        if form.validate():
            form.save()
            flash('Payment options updated')

    return render_template('settings/payment_integration.html', form=form)
