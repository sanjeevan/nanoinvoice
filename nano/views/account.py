# -*- coding: utf-8 -*-

from uuid import uuid4
from datetime import datetime

from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, g, abort)
from flask.ext.mail import Message
from flaskext.babel import gettext as _
from flask.ext.login import (login_required, login_user, current_user,
                            logout_user, confirm_login, fresh_login_required,
                            login_fresh)

from nano.models import User, Company, CustomField, Plan, Subscription
from nano.extensions import db, cache, mail, login_manager
from nano.forms import (SignupForm, LoginForm, RecoverPasswordForm,
                        ChangePasswordForm, ReauthForm, UserForm, BusinessForm,
                        CustomFieldForm, SubscribeForm)
from nano.utils import Struct

account = Blueprint('account', __name__, url_prefix='/account')

@account.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Account information + update"""
    user = User.query.get(current_user.id)
    form = UserForm(request.form, obj=user)

    if request.method == 'POST' and form.validate():
        form.save()
        flash('User information updated')

    return render_template('account/index.html', form=form)

@account.route('/business', methods=['GET', 'POST'])
@login_required
def business():
    """Company information + update"""
    company = Company.query.filter_by(user_id=current_user.id).first()
    form = BusinessForm(request.form, obj=company)

    if request.method == 'POST' and form.validate():
        company = form.save()
        flash('Business details updated')

    return render_template('account/business.html', form=form, company=company)

@account.route('/subscription', methods=['GET'])
def subscription():
    """Subscription information"""
    plan = current_user.subscription.plan
    transactions = current_user.subscription.transactions

    return render_template('account/subscription.html', plan=plan,
                                                        transactions=transactions)

@account.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Application settings"""
    custom_fields = CustomField.query.filter_by(user_id=current_user.id).all() 
    form = CustomFieldForm(request.form)

    if request.method == 'POST' and form.validate():
        custom_field = form.save()
        flash('New custom field added')
        return redirect(request.referrer)
    else:
        print form.errors

    return render_template('account/settings.html', form=form,
                                                    fields=custom_fields)

@account.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(login=request.args.get('login', None),
                     next=request.args.get('next', None))

    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.login.data,
                                    form.password.data)

        if user and authenticated:
            remember = request.form.get('remember') == 'y'
            if login_user(user, remember=remember):
                flash("Logged in!", 'success')
            return redirect(form.next.data or url_for('home.index'))
        else:
            flash(_('Sorry, invalid login'), 'error')

    return render_template('account/login.html', form=form)


@account.route('/reauth', methods=['GET', 'POST'])
@login_required
def reauth():
    form = ReauthForm(next=request.args.get('next'))

    if request.method == 'POST':
        user, authenticated = User.authenticate(current_user.name,
                                    form.password.data)
        if user and authenticated:
            confirm_login()
            current_app.logger.debug('reauth: %s' % session['_fresh'])
            flash(_('Reauthenticated.'), 'success')
            return redirect('/change_password')

        flash(_('Password is wrong.'), 'error')
    return render_template('reauth.html', form=form)

@account.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    flash(_('You are now logged out'), 'success')
    return redirect(url_for('home.index'))

@account.route('/signup', methods=['GET', 'POST'])
def signup():
    """Create a new account"""
    login_form= LoginForm(next=request.args.get('next'))
    form = SignupForm(request.form, next=request.args.get('next'))

    if form.validate_on_submit():
        user, subscription = form.save()
        if user.subscription.plan.name == 'Free':
            login_user(user)
            return redirect(form.next.data or url_for('home.dashboard'))
        if user.subscription.plan.name == 'Pro':
            login_user(user)
            return redirect(url_for('account.subscribe', plan_id=user.subscription.plan.id))
    else:
        print form.errors
        print "unable to validate"

    return render_template('account/signup.html', 
                           form=form, 
                           login_form=login_form)

@account.route('/subscribe/<int:plan_id>', methods=['GET', 'POST'])
def subscribe(plan_id):
    """Subscribe to a plan"""
    # don't allow user to subscribe to an already subscribed plan
    if (current_user.subscription.active and
        plan_id == current_user.subscription.plan_id):
        return redirect(url_for('home.dashboard'))

    plan = Plan.query.get(plan_id)
    if not plan:
        return 'Plan not found', 404

    obj = Struct(**{'plan_id': plan.id, 'name': current_user.name})
    form = SubscribeForm(request.form, obj=obj)
    if request.method == 'POST':
        if form.validate():
            subscription = form.create_subscription(current_user)
            if subscription:
                flash('You have successfully subscribed to the %s plan' % plan.name)
                return redirect(url_for('account.subscription'))
        else:
            return 'there were errors', 400
    return render_template('account/subscribe.html', plan=plan, form=form)

@account.route('/subscribe/downgrade_to_free', methods=['GET', 'POST'])
def downgrade_to_free():
    """Downgrade to a free account"""
    if not current_user.subscription.active:
        subscription = Subscription.query.get(current_user.subscription.id)
        free_plan = Plan.query.filter_by(name='Free').first()
        subscription.plan_id = free_plan.id
        db.session.commit()
    return redirect(url_for('home.dashboard'))

@account.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """Change user password"""
    user = None
    if current_user.is_authenticated():
        if not login_fresh():
            return login_manager.needs_refresh()
        user = current_user
    elif 'activation_key' in request.values and 'email' in request.values:
        activation_key = request.values['activation_key']
        email = request.values['email']
        user = User.query.filter_by(activation_key=activation_key) \
                         .filter_by(email=email).first()

    if user is None:
        abort(403)

    form = ChangePasswordForm(activation_key=user.activation_key)

    if form.validate_on_submit():
        user.password = form.password.data
        user.activation_key = None
        db.session.add(user)
        db.session.commit()

        flash(_("Your password has been changed, please log in again"),
              "success")
        return redirect(url_for("account.login"))

    return render_template("change_password.html", form=form)

@account.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = RecoverPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash(_('Please see your email for instructions on how to access your account'), 'success')

            user.activation_key = str(uuid4())
            db.session.add(user)
            db.session.commit()

            body = render_template('emails/reset_password.html', user=user)
            message = Message(subject=_('Recover your password'), body=body,
                              recipients=[user.email])
            mail.send(message)

            return redirect(url_for('account.index'))
        else:
            flash(_('Sorry, no user found for that email address'), 'error')

    return render_template('reset_password.html', form=form)

