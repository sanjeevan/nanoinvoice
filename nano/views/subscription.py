"""Subscriptions"""

import stripe
from datetime import datetime
from flask import (Blueprint, render_template, request,
                   flash, url_for, redirect, current_app)
from flask.ext.login import login_required, current_user
from nano.models import Plan, Subscription
from nano.extensions import db
from nano.forms import SubscribeForm
from nano.utils import Struct

subscription = Blueprint('subscription', __name__, url_prefix='/subscription')

@subscription.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Subscription information"""
    plan = current_user.subscription.plan
    transactions = current_user.subscription.transactions

    return render_template('subscription/index.html', plan=plan,
                                                        transactions=transactions)

@subscription.route('/create/<int:plan_id>', methods=['GET', 'POST'])
def create(plan_id):
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
                return redirect(url_for('subscription.index'))
        else:
            return 'there were errors', 400
    return render_template('subscription/create.html', plan=plan, form=form)

@subscription.route('/downgrade_to_free', methods=['GET', 'POST'])
def downgrade_to_free():
    """Downgrade to a free account"""
    if not current_user.subscription.active:
        subscription = Subscription.query.get(current_user.subscription.id)
        free_plan = Plan.query.filter_by(name='Free').first()
        subscription.plan_id = free_plan.id
        db.session.commit()
    return redirect(url_for('home.dashboard'))

@subscription.route('/cancel', methods=['GET', 'POST'])
def cancel():
    subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    if not subscription.active:
        return redirect(request.referrer)
    if request.method == 'POST':
        if subscription.cancel():
            flash('Your subscription has been cancelled')
        return redirect(url_for('subscription.index'))

    return render_template('subscription/cancel.html', subscription=subscription)
