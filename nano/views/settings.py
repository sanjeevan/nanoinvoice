# -*- coding: utf-8 -*-

from uuid import uuid4
from datetime import datetime

from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, g, abort)
from flask.ext.login import current_user, login_required

from nano.models import User, Company, CustomField
from nano.extensions import db
from nano.forms import CustomFieldForm

settings = Blueprint('settings', __name__, url_prefix='/settings')

@settings.route('/', methods=['GET', 'POST'])
def index():
    return render_template('settings/index.html')

@settings.route('/custom_fields', methods=['GET', 'POST'])
@login_required
def custom_fields():
    """Application settings"""
    custom_fields = CustomField.query.filter_by(user_id=current_user.id).all() 
    form = CustomFieldForm(request.form)

    if request.method == 'POST' and form.validate():
        custom_field = form.save()
        flash('New custom field added')
        return redirect(request.referrer)
    else:
        print form.errors

    return render_template('settings/custom_fields.html', form=form,
                                                          fields=custom_fields)
