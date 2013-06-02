"""Stripe related models"""

from datetime import datetime
from nano.extensions import db

class StripeAccount(db.Model):
    __tablename__ = 'stripe_account'

    id = db.Column(db.Integer(11), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer(11), db.ForeignKey('user.id'))
    secret_key = db.Column(db.Unicode(255))
    public_key = db.Column(db.Unicode(255))
    enabled = db.Column(db.Boolean, default=False)

    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    @classmethod
    def get_or_create_for_user(cls, user_id):
        account = cls.query.filter_by(user_id=user_id).first()
        if not account:
            model = cls()
            model.user_id = user_id
            db.session.add(model)
            db.session.commit()
        return account

class StripePayment(db.Model):
    __tablename__ = 'stripe_payment'

    id = db.Column(db.Integer(11), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer(11), db.ForeignKey('user.id'))
    payment_id = db.Column(db.Integer(11), db.ForeignKey('payment.id'))

    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    @classmethod
    def get_or_create_for_user(cls, user_id):
        account = cls.query.filter_by(user_id=user_id).first()
        if not account:
            model = cls()
            model.user_id = user_id
            db.session.add(model)
            db.session.commit()
        return account


