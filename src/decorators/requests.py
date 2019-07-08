from functools import wraps

from flask import request

from src.utils import ResponseGenerator


def json_data_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not request.is_json:
            return ResponseGenerator.json_data_expected()

        try:
            request.get_json()
        except Exception as _e:
            return ResponseGenerator.json_data_expected()

        return f(*args, **kwargs)

    return wrap
