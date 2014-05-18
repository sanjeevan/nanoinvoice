"""Dynamically generated javascript"""
import json

from flask import Blueprint, render_template, request, current_app
from nano.models import WebhookLog, Subscription, Transaction
from nano.extensions import db

webhook = Blueprint('webhook', __name__, url_prefix='/webhook')

def _log_request():
    # log the request
    log = WebhookLog()
    log.service = 'stripe'
    log.ip = request.remote_addr
    log.data = json.dumps(request.json)
    log.headers = json.dumps(request.headers.to_list())

    db.session.add(log)
    db.session.commit()

def _create_transaction(subscription, obj):
    trans = Transaction()
    trans.user_id = subscription.user_id
    trans.subscription_id = subscription.id
    trans.success = True
    trans.amount = float(obj['total'])/100
    trans.charge_id = obj['charge']
    db.session.add(trans)
    db.session.commit()

@webhook.route('/', methods=['GET', 'POST'])
def index():
    """Main webhook endpoint for stripe"""
    if not request.json:
        return 'error', 500

    if not request.args.get('_no_store'):
        _log_request()
    _type = request.json['type']
    current_app.logger.info('Received webhook %s' % _type)

    if _type == 'invoice.payment_succeeded':
        customer_id = request.json['data']['object']['customer']
        subscription_id = request.json['data']['object']['subscription']
        subscription = Subscription.query.filter_by(stripe_customer_id=customer_id) \
                                         .filter_by(stripe_subscription_id=subscription_id) \
                                         .first()
        if subscription:
            _create_transaction(subscription, request.json['data']['object'])

    if _type == 'invoice.payment_failed':
        pass

    if _type == 'customer.subscription.deleted':
        pass

    if _type == 'customer.subscription.updated':
        pass

    if _type == 'customer.deleted':
        pass

    return 'ok'
