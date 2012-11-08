from flask import Flask, Blueprint, render_template, abort, redirect, url_for, request
from jinja2 import TemplateNotFound
from flask.ext.login import login_required, current_user

from nano.models import Contact
from nano.forms import DetailedClientForm

client = Blueprint('client', __name__, url_prefix='/client')

@client.route('/', methods=['GET'])
@login_required
def index():
    contacts = Contact.query.filter_by(user_id=current_user.id).all()
    return render_template('client/index.html', contacts=contacts)

@client.route('/<int:id>', methods=['GET'])
def show():
    return render_template('client/show.html')

@client.route('/create', methods=['GET', 'POST'])
def create():
    form = DetailedClientForm(request.form)
    
    if request.method == 'POST' and form.validate():
        pass

    return render_template('client/create.html', form=form)

@client.route('/<int:id>/delete', methods=['GET'])
def delete():
    pass
