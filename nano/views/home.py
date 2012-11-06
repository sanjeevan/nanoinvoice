from flask import Flask, Blueprint, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound
from flask.ext.login import login_required, current_user

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated():
        return redirect('/dashboard')

    return render_template('home/index.html')

@home.route('/login')
def login():
    return redirect(url_for('account.login'))

@home.route('/dashboard')
@login_required
def dashboard():
    return render_template('home/dashboard.html', user=current_user)
