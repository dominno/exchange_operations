import json


def query_to_json(query):
    out = []
    for item in query:
        out.append(item.as_dict())
    return json.dumps(out)
