import pytest

from decimal import Decimal
from exchange_operations.api.operatations.utils import get_latest_currency_rate, OpenExchangeRatesError


def test_should_be_able_to_get_latest_currency_rates(test_app, patch_request_get):
    latest, last_updated = get_latest_currency_rate('EUR')
    assert latest == Decimal("0.85070600")


def test_wrong_currency_code_should_raise_exception(test_app, patch_request_get):
    with pytest.raises(OpenExchangeRatesError) as excinfo:
        latest, last_updated = get_latest_currency_rate('WRONG')
    assert "Error getting latest rates from openexchangerates, currency_code" in str(excinfo.value)
