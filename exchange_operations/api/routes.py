routes = [
    ('exchange_operations.api.operatations.views.LastOperationResource', [
        '/exchange_operations/last',
        '/exchange_operations/last/<string:currency_code>',
        '/exchange_operations/last/<int:operations_count>',
        '/exchange_operations/last/<string:currency_code>/<int:operations_count>',
    ]),
    ('exchange_operations.api.operatations.views.GetAndSaveResource', [
        '/exchange_operations/add'
    ])
]
