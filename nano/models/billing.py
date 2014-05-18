"""Application billing"""
import stripe

from datetime import datetime
from flask import current_app

from nano.extensions import db

class Plan(db.Model):
    __tablename__ = 'plan'

    id          = db.Column(db.Integer, primary_key=True, nullable=False)
    name        = db.Column(db.Unicode(20))
    gateway_uid = db.Column(db.Unicode(255))
    description = db.Column(db.Unicode(255))
    amount      = db.Column(db.Numeric(8, 2), default=0)
    billing_interval = db.Column(db.Enum('daily', 'weekly', 'monthly', 'yearly'), default='monthly')

    created_at  = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # relationships
    subscriptions = db.relation('Subscription', backref=db.backref('plan', uselist=False))

    @property
    def interval_name(self):
        if self.billing_interval == 'monthly':
            return 'month'

class Subscription(db.Model):
    __tablename__ = 'subscription'
    id                      = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id                 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id                 = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    active                  = db.Column(db.Boolean, nullable=False, default=False)
    start_date              = db.Column(db.DateTime, nullable=True)
    end_date                = db.Column(db.DateTime, nullable=True)
    stripe_data             = db.Column(db.UnicodeText(4294967295), nullable=False, default=u'{}')
    stripe_customer_id      = db.Column(db.Unicode(255), nullable=True)
    stripe_subscription_id  = db.Column(db.Unicode(255), nullable=True)
    updated_at              = db.Column(db.DateTime, nullable=False, default=datetime.now)
    created_at              = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # relations
    transactions = db.relation('Transaction', backref=db.backref('subscription', lazy='joined', uselist=False))

    def cancel(self):
        try:
            stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
            customer_obj = stripe.Customer.retrieve(self.stripe_customer_id)
            customer_obj.subscriptions.retrieve(self.stripe_subscription_id).delete()
        except stripe.error.InvalidRequestError as e:
            current_app.logger.error('Problem with cancelling subscription %s: %s' % (self.id, str(e)))
            return False

        self.active = False
        free_plan = Plan.query.filter_by(name='Free').first()
        self.plan_id = free_plan.id
        self.end_date = datetime.now()
        db.session.commit()
        return True

class Transaction(db.Model):
    __tablename__ = 'transaction'

    id              = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False)
    success         = db.Column(db.Boolean, default=False)
    amount          = db.Column(db.Numeric(8, 2), default=0)
    charge_id       = db.Column(db.Unicode(100), nullable=True)
    charge          = db.Column(db.UnicodeText(4294967295), nullable=True)

    updated_at  = db.Column(db.DateTime, nullable=False, default=datetime.now)
    created_at  = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


