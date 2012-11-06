from flask import Flask, Blueprint, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound
from flask.ext.login import login_required, current_user
from nano.models import Contact

client = Blueprint('client', __name__, url_prefix='/client')

@client.route('/', methods=['GET'])
@login_required
def index():
    contacts = Contact.query.filter_by(user_id=current_user.id).all()
    return render_template('client/index.html', contacts=contacts)


@client.route('/<int:id>', methods=['GET'])
def show():
    pass

@client.route('/create', methods=['GET', 'POST']
def create():
    pass


@client.route('/<int:id>/delete', methods=['GET'])
def delete():
    pass
