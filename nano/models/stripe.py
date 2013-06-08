"""Stripe related models"""

from datetime import datetime

from nano.models.payment import Payment
from nano.extensions import db

class StripeAccount(db.Model):
    __tablename__ = 'stripe_account'

    id          = db.Column(db.Integer(11), primary_key=True, nullable=False)
    user_id     = db.Column(db.Integer(11), db.ForeignKey('user.id'))
    secret_key  = db.Column(db.Unicode(255))
    public_key  = db.Column(db.Unicode(255))
    enabled     = db.Column(db.Boolean, default=False)

    updated_at  = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    created_at  = db.Column(db.DateTime(), nullable=False, default=datetime.now)

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

    id              = db.Column(db.Integer(11), primary_key=True, nullable=False)
    user_id         = db.Column(db.Integer(11), db.ForeignKey('user.id'), nullable=False)
    payment_id      = db.Column(db.Integer(11), db.ForeignKey('payment.id'), nullable=True)
    invoice_id      = db.Column(db.Integer(11), db.ForeignKey('invoice.id'), nullable=False)
    amount          = db.Column(db.Numeric(8, 2), default=0)
    token           = db.Column(db.Unicode(100), nullable=False)
    state           = db.Column(db.Unicode(20), default=u'initialized')
    error_message   = db.Column(db.Unicode(255), nullable=True)
    charge_id       = db.Column(db.Unicode(100), nullable=True)
    charge          = db.Column(db.UnicodeText(4294967295), nullable=False, default=u'{}')
    created_at      = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    @classmethod
    def get_or_create_for_user(cls, user_id):
        account = cls.query.filter_by(user_id=user_id).first()
        if not account:
            model = cls()
            model.user_id = user_id
            db.session.add(model)
            db.session.commit()
        return account

    def create_payment_object(self):
        """Create related payment object"""
        payment = Payment()
        payment.invoice_id = self.invoice_id
        payment.date = datetime.now()
        payment.currency_code = self.invoice.currency_code
        payment.amount = self.amount
        payment.method = 'stripe'
        payment.description = 'Credit card payment'

        db.session.add(payment)
        db.session.commit()

        return payment

