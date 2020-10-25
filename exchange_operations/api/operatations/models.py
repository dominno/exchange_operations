import json

from exchange_operations import db_sql_alchemy as db


class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), nullable=False, index=True)
    amount_requested = db.Column(db.Numeric(precision=65, scale=8, asdecimal=True))
    exchange_price = db.Column(db.Numeric(precision=65, scale=8, asdecimal=True))
    final_amount = db.Column(db.Numeric(precision=65, scale=8, asdecimal=True))
    date = db.Column(db.DateTime, index=True)

    __table_args__ = (
        db.Index('operation_currency_date_idx', currency, date.desc()),
    )

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    def as_dict(self):
        return {
            'id': self.id,
            'currency': self.currency,
            'amount_requested': str(self.amount_requested),
            'exchange_price': str(self.exchange_price),
            'final_amount': str(self.final_amount),
            'date': str(self.date)
        }

    def as_json(self):
        return json.dumps(self.as_dict())
