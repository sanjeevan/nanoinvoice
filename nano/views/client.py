from flask import (Flask, Blueprint, render_template, abort, redirect, url_for,
                   request, flash)
from jinja2 import TemplateNotFound
from flask.ext.login import login_required, current_user

from nano.models import Contact
from nano.forms import SimpleClientForm, DetailedClientForm
from nano.utils import Struct
from nano.extensions import db

client = Blueprint('client', __name__, url_prefix='/client')

@client.route('/', methods=['GET'])
@login_required
def index():
    contacts = Contact.query.filter_by(user_id=current_user.id).all()
    return render_template('client/index.html', contacts=contacts)

@client.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def show(id):
    contact = Contact.query.get(id)
    if not contact:
        return 'Contact not found', 404
    form = DetailedClientForm(request.form, obj=contact)
    
    if request.method == 'POST' and form.validate():
        form.save()
        flash('Client details updated')

    return render_template('client/show.html', contact=contact, form=form)

@client.route('/update/<int:id>', methods=['POST'])
def update(id):
    pass

@client.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = SimpleClientForm(request.form)
    
    if request.method == 'POST' and form.validate():
        client = form.save()
        flash('New client created')
        return redirect(url_for('.index'))

    return render_template('client/create.html', form=form)

@client.route('/<int:id>/delete', methods=['GET'])
@login_required
def delete(id):
    contact = Contact.query.get(id)
    if contact:
        db.session.delete(contact)
        db.session.commit()
        flash('Client deleted')
    return redirect(url_for('.index'))
