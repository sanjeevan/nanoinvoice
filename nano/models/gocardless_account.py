"""GoCardless related models"""

from datetime import datetime
from nano.extensions import db

from nano.models.payment import Payment

class GoCardlessAccount(db.Model):
    __tablename__ = 'gocardless_account'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    app_identifier = db.Column(db.Unicode(255))
    app_secret = db.Column(db.Unicode(255))
    merchant_access_token = db.Column(db.Unicode(255))
    merchant_id = db.Column(db.Unicode(255))
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

class GoCardlessPayment(db.Model):
    __tablename__ = 'gocardless_payment'

    id            = db.Column(db.Integer, primary_key=True, nullable=False)
    invoice_id    = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    user_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    payment_id    = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=True)
    amount        = db.Column(db.Numeric(8, 2), default=0)
    reference     = db.Column(db.Unicode(100), nullable=False)
    state         = db.Column(db.Unicode(20), default=u'initialized')
    resource_id   = db.Column(db.Unicode(100), nullable=True)
    resource_uri  = db.Column(db.Unicode(255), nullable=True)
    error_message = db.Column(db.Unicode(255), nullable=True)

    created_at  = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    def create_payment_object(self):
        """Create related payment object"""
        payment = Payment()
        payment.invoice_id = self.invoice_id
        payment.date = datetime.now()
        payment.currency_code = self.invoice.currency_code
        payment.amount = self.amount
        payment.method = 'gocardless'
        payment.description = 'Direct debit payment'

        db.session.add(payment)
        db.session.commit()

        return payment
