"""Dynamically generated javascript"""
import json

from flask import Blueprint, render_template, request
from nano.models import WebhookLog
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

@webhook.route('/', methods=['GET', 'POST'])
def index():
    """Main webhook endpoint for stripe"""
    _log_request()

    if not request.json:
        return 'error', 500

    _type = request.json['type']

    if _type == 'invoice.payment_succeeded':
        pass

    if _type == 'invoice.payment_failed':
        pass

    if _type == 'customer.subscription.deleted':
        pass

    if _type == 'customer.subscription.updated':
        pass

    if _type == 'customer.deleted':
        pass

    return 'ok'
