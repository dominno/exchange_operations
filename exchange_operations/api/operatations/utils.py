import requests
import decimal
from flask import current_app

from datetime import datetime


class OpenExchangeRatesError(Exception):
    pass


def get_latest():
    url = "https://openexchangerates.org/api/latest.json?app_id=%s" % current_app.config['OPENEXCHANGERATES_APP_ID']
    return requests.get(url).json()


def get_latest_currency_rate(currency_code):
    try:
        latest = get_latest()
        return quantize(latest["rates"][currency_code]), datetime.fromtimestamp(latest['timestamp'])
    except KeyError:
        raise OpenExchangeRatesError('Error getting latest rates from openexchangerates, currency_code %s not found' % currency_code)


def quantize(value, places=8):
    '''
    Adds missing zeros to the value, so it has always have precision of 8 decimal digits
    0.850706 will make 0.85070600
    '''
    prec = decimal.Decimal(10) ** -places
    return decimal.Decimal(value).quantize(prec, rounding=decimal.ROUND_UP)
