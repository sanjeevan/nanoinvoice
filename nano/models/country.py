from datetime import datetime
from nano.extensions import db

class Country(db.Model):
    __tablename__ = 'country'

    #column definitions
    id              = db.Column(u'id', db.BigInteger, primary_key=True, nullable=False)
    iso             = db.Column(u'iso', db.String(length=100))
    name            = db.Column(u'name', db.String(length=100))
    printable_name  = db.Column(u'printable_name', db.String(length=100))
    iso3            = db.Column(u'iso3', db.String(length=100))
