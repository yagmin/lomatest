import datetime
import uuid
import json
from flask import jsonify
from sqlalchemy.dialects import postgresql


def alchemy_encoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    instanceof = type(obj)

    if instanceof in [datetime.datetime, datetime.date, datetime.time]:
        return obj.isoformat()
    elif instanceof == datetime.timedelta:
        return (datetime.datetime.min + obj).time().isoformat()
    elif instanceof == uuid.UUID:
        return obj.hex

    return obj


def json_dict(d):
    json_obj = json.dumps(d, default=alchemy_encoder)
    return jsonify(json.loads(json_obj))


def row_to_dict(row):
    dict_row = dict(row.__dict__)
    dict_row.pop('_sa_instance_state', None)
    return dict_row


def row_to_json(row):
    dict_row = row_to_dict(row)
    return json_dict(dict_row)


def print_query(query):
    print(str(query.statement.compile(dialect=postgresql.dialect())))
