import json

from ..api.operatations.models import Operation


def test_should_be_able_to_store_latest_exchanage_operation(test_app, patch_request_get, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/exchange_operations/add",
        data=json.dumps({"currency_code": "AUD", "amount": 100}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert data["currency"] == "AUD"
    assert data["amount_requested"] == "100.00000000"
    assert data["exchange_price"] == "1.39639100"
    assert data["final_amount"] == "139.63910000"
    assert data["date"] == '2020-10-08 13:00:00'
    assert len(Operation.query.all()) == 1


def test_no_params_passed_should_return_400(test_app, patch_request_get, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/exchange_operations/add",
        content_type="application/json",
    )
    assert resp.status_code == 400


def test_operation_should_not_be_stored_if_it_already_exist_for_date_and_currency(test_app, patch_request_get, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/exchange_operations/add",
        data=json.dumps({"currency_code": "AUD", "amount": 100}),
        content_type="application/json",
    )
    resp = client.post(
        "/exchange_operations/add",
        data=json.dumps({"currency_code": "AUD", "amount": 100}),
        content_type="application/json",
    )
    assert len(Operation.query.all()) == 1


def test_should_be_able_to_fetch_last_operation(test_app, operations):
    client = test_app.test_client()
    resp = client.get(
        "/exchange_operations/last",
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert len(data) == 1
    assert data[0]['date'] == '2020-10-01 14:55:00'


def test_should_be_able_to_fetch_last_operation_for_currecy(test_app, operations):
    client = test_app.test_client()
    resp = client.get(
        "/exchange_operations/last/EUR",
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert len(data) == 1
    assert data[0]['date'] == '2020-10-01 13:50:00'
    assert data[0]['currency'] == 'EUR'


def test_should_be_able_to_fetch_number_of_last_operations(test_app, operations):
    client = test_app.test_client()
    resp = client.get(
        "/exchange_operations/last/2",
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert len(data) == 2
    assert data[0]['date'] == '2020-10-01 14:55:00'
    assert data[1]['date'] == '2020-10-01 13:50:00'
    assert data[0]['currency'] == 'AUD'
    assert data[1]['currency'] == 'EUR'


def test_should_be_able_to_fetch_number_of_last_operations_for_currecy(test_app, operations):
    client = test_app.test_client()
    resp = client.get(
        "/exchange_operations/last/EUR/2",
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert len(data) == 2
    assert data[0]['date'] == '2020-10-01 13:50:00'
    assert data[1]['date'] == '2020-09-01 12:50:00'
    assert data[0]['currency'] == 'EUR'
    assert data[1]['currency'] == 'EUR'


def test_should_be_able_to_pass_currency_as_lower_case(test_app, operations):
    client = test_app.test_client()
    resp = client.get(
        "/exchange_operations/last/eur",
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert len(data) == 1
    assert data[0]['date'] == '2020-10-01 13:50:00'
    assert data[0]['currency'] == 'EUR'
