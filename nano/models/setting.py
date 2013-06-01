"""Setting model + manager"""

import json

from datetime import datetime
from nano.extensions import db

class Setting(db.Model):
    __tablename__ = 'setting'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))

    key = db.Column(db.Unicode(100))
    value = db.Column(db.BLOB())

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    def set_value(self, value):
        self.value = json.dumps(value)

    def get_value(self):
        return json.loads(self.value)

class SettingManager(object):
    def __init__(self, user):
        self.user = user

    def get_val(self, name, default=None):
        setting = Setting.query.filter_by(user_id=self.user.id) \
                               .filter_by(key=name) \
                               .first()
        if setting:
            return setting.get_value()
        else:
            default

    def set_val(self, name, val=None):
        setting = Setting.query.filter_by(user_id=self.user.id) \
                               .filter_by(key=name) \
                               .first()
        if setting:
            setting.set_value(val)
            db.session.commit()
        else:
            setting = Setting()
            setting.user_id = self.user.id
            setting.key = name
            setting.set_value(val)
            db.session.add(setting)
            db.session.commit()
        return setting


