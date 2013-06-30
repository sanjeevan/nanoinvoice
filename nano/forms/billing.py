"""Forms for billing/subscription"""

import stripe
import json

from datetime import datetime
from flask import current_app
from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          SubmitField, SelectField, FormField,
                          ValidationError, required, equal_to, email,
                          length)

from nano.models import Plan
from nano.extensions import db

class SubscribeForm(Form):
    """Get basic credit card info"""

    name            = TextField(u'Card number', [required()])
    card_number     = TextField(u'Card number', [required()])
    cvc             = TextField(u'CVC', [required()])
    expire_month    = SelectField(u'Expire month', [required()])
    expire_year     = SelectField(u'Expire year', [required()])
    stripe_token    = HiddenField(u'Stripe token', [required()])
    plan_id         = HiddenField(u'Plan', [required()])

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(SubscribeForm, self).__init__(formdata, obj, prefix, **kwargs)

        self.expire_month.choices = self.get_months()
        self.expire_year.choices = self.get_years()

    def get_years(self):
        ahead = 20
        year = datetime.now().year
        return [(str(y), str(y)) for y in xrange(year, year+ahead)]

    def get_months(self):
        return [(str(i), str(i)) for i in xrange(1, 13)]

    def create_subscription(self, user):
        """Create the stripe subscription"""
        plan = Plan.query.get(self.plan_id.data)
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        
        try:
            customer = stripe.Customer.create(
                card=self.stripe_token.data,
                plan=plan.gateway_uid,
                email=user.email_address
            )
        except stripe.CardError as e:
            return False

        data = {'customer': json.loads(str(customer)) }
        user.subscription.plan_id = plan.id
        user.subscription.stripe_data = json.dumps(data)
        user.subscription.active = True
        db.session.add(user.subscription)
        db.session.commit()
        return True

