import urllib, hashlib

from werkzeug import (generate_password_hash, check_password_hash,
                      cached_property)
from flask.ext.login import UserMixin

from nano.extensions import db
from nano.utils import get_current_time, VARCHAR_LEN_128
from nano.models.setting import SettingManager

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email_address = db.Column(db.String(VARCHAR_LEN_128), nullable=False, unique=True)
    _password = db.Column('password', db.String(VARCHAR_LEN_128), nullable=False)
    is_active_account = db.Column(db.Boolean, default=True)
    is_super_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, default=0)
    created_at = db.Column(db.DateTime, default=get_current_time())
    updated_at = db.Column(db.DateTime, default=get_current_time())

    # relations
    invoice_links = db.relation('InvoiceLink', backref=db.backref('user', uselist=False))

    @property
    def setting(self):
        return SettingManager(self)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    # Hide password encryption by exposing password field only.
    password = db.synonym('_password', descriptor=property(_get_password,
                                                           _set_password))

    def __repr__(self):
        return '<User %r>' % self.username

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(db.or_(User.username==login, 
                                       User.email_address==login)).first()
        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    @classmethod
    def search(cls, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(
                User.name.ilike(keyword),
                User.email.ilike(keyword),
            ))
        q = reduce(db.and_, criteria)
        return cls.query.filter(q)


    def gravatar_url(self, size=40):
        g_url = 'http://www.gravatar.com/avatar/' + hashlib.md5(unicode(self.email_address).lower()).hexdigest()
        g_url+= '?' + urllib.urlencode({'s': str(size)})
        return g_url



