"""
    Utils has nothing to do with models and views.
"""

from datetime import datetime

import json
import decimal
import random

VARCHAR_LEN_128 = 128
ALPHABET = "bcdfghjklmnpqrstvwxyz0123456789BCDFGHJKLMNPQRSTVWXYZ"

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

def json_dumps(obj):
    class DateTimeJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, decimal.Decimal):
                return float(obj)
            else:
                return super(DateTimeJSONEncoder, self).default(obj)
    return json.dumps(obj, cls=DateTimeJSONEncoder)

def model_to_dict(model):
    d = {}
    for c in model.__table__.columns:
        val = getattr(model, c.name)
        d[c.name] = val
    return d
    
def get_current_time():
    return datetime.utcnow()

def pretty_date(dt, default=None):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    Ref: https://bitbucket.org/danjac/newsmeme/src/a281babb9ca3/newsmeme/
    """

    if default is None:
        default = 'just now'

    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds'),
    )

    for period, singular, plural in periods:

        if not period:
            continue

        if period == 1:
            return u'%d %s ago' % (period, singular)
        else:
            return u'%d %s ago' % (period, plural)

    return default

def random_id(length):
    return ''.join([random.choice(ALPHABET) for i in xrange(length)])

