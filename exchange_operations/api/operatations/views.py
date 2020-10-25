from flask_restful import reqparse, abort, Api, Resource

from exchange_operations.api.utils import query_to_json
from .utils import get_latest_currency_rate, quantize
from .models import Operation

from flask import Response


parser = reqparse.RequestParser()
parser.add_argument('currency_code', type=str, help='Currency code')
parser.add_argument('amount', type=float, help='Amount that will be used to multiply the exchange price')


class GetAndSaveResource(Resource):

    def post(self):
        args = parser.parse_args()
        try:
            exchange_price, last_updated = get_latest_currency_rate(args['currency_code'])
        except Exception as err:
            abort(400, message=str(err))
        existing_price = Operation.query.filter_by(currency=args['currency_code'], date=last_updated).first()
        if existing_price:
            return Response(existing_price.as_json(), mimetype="application/json", status=200)

        amount_requested = quantize(args['amount'])
        new_price = Operation.create(
            currency=args['currency_code'], amount_requested=str(amount_requested),
            exchange_price=str(exchange_price), final_amount=str(quantize(exchange_price * amount_requested)),
            date=last_updated
        )
        return Response(new_price.as_json(), mimetype="application/json", status=201)


class LastOperationResource(Resource):

    def get(self, currency_code=None, operations_count=1):
        qs = Operation.query
        if currency_code:
            qs = qs.filter_by(currency=currency_code)
        qs = qs.order_by(Operation.date.desc()).limit(operations_count).all()
        return Response(query_to_json(qs), mimetype="application/json", status=200)
