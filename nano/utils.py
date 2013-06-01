"""
    Utils has nothing to do with models and views.
"""

from datetime import datetime

import math
import json
import decimal

VARCHAR_LEN_128 = 128
ALPHABET = "bcdfghjklmnpqrstvwxyz0123456789BCDFGHJKLMNPQRSTVWXYZ"
BASE = len(ALPHABET)
MAXLEN = 6

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

def encode_id(n):
    pad = MAXLEN - 1
    n = int(n + pow(BASE, pad))

    s = []
    t = int(math.log(n, BASE))
    while True:
        bcp = int(pow(BASE, t))
        a = int(n / bcp) % BASE
        s.append(ALPHABET[a:a+1])
        n = n - (a * bcp)
        t -= 1
        if t < 0: break

    return "".join(reversed(s))

def decode_id(n):
    n = "".join(reversed(n))
    s = 0
    l = len(n) - 1
    t = 0
    while True:
        bcpow = int(pow(BASE, l - t))
        s = s + ALPHABET.index(n[t:t+1]) * bcpow
        t += 1
        if t > l: break

    pad = MAXLEN - 1
    s = int(s - pow(BASE, pad))

    return int(s)
