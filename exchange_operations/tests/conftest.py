import pytest
import requests

from datetime import datetime

from sqlalchemy_utils import database_exists, create_database, drop_database

from exchange_operations.api.operatations.models import Operation
from exchange_operations import create_app
from exchange_operations import db_sql_alchemy as db



@pytest.fixture(scope="module")
def test_app():
    app = create_app("exchange_operations.config.TestingConfig")
    with app.app_context():
        yield app  # testing happens here


@pytest.fixture(scope="function")
def test_database(test_app):
    if not database_exists(test_app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(test_app.config['SQLALCHEMY_DATABASE_URI'])
    else:
        db.drop_all()
    db.create_all()
    yield db  # testing happens here
    db.session.remove()
    db.drop_all()


@pytest.fixture()
def openexchangerates_output():
    return {'disclaimer': 'Usage subject to terms: https://openexchangerates.org/terms', 'license': 'https://openexchangerates.org/license', 'timestamp': 1602162000, 'base': 'USD', 'rates': {'AUD': 1.396391, 'EUR': 0.850706}}


@pytest.fixture()
def patch_request_get(monkeypatch, openexchangerates_output):
    class MockResponse:
        @staticmethod
        def json():
            return openexchangerates_output

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture()
def operations(test_database):
    to_insert = [
        {
            'currency_code': 'EUR', 'amount_requested': "1.5", 'exchange_price': '0.85070600', 'final_amount': '1.27605900',
            'date': datetime(2020, 9, 1, 12, 50)
        },
        {
            'currency_code': 'AUD', 'amount_requested': "2", 'exchange_price': '1.00000000',
            'final_amount': '2.00000000',
            'date': datetime(2020, 10, 1, 12, 55)
        },
        {
            'currency_code': 'EUR', 'amount_requested': "1.5", 'exchange_price': '0.85070600', 'final_amount': '1.27605900',
            'date': datetime(2020, 10, 1, 13, 50)
        },
        {
            'currency_code': 'AUD', 'amount_requested': "2", 'exchange_price': '1.00000000',
            'final_amount': '2.00000000',
            'date': datetime(2020, 10, 1, 14, 55)
        },
    ]
    for price in to_insert:
        Operation.create(
            currency=price['currency_code'], amount_requested=price['amount_requested'],
            exchange_price=price['exchange_price'], final_amount=price['final_amount'],
            date=price['date']
        )
