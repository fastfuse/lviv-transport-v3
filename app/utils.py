# -*- coding: utf-8 -*-

from collections import namedtuple
from functools import wraps

from flask import request, make_response, jsonify
from app import models


# namedtuple to simplify creation of response messages
Response = namedtuple('Response', ['status', 'message'])


def login_required(func):
    """
    Login required decorator.
    Additionally gives access to User object inside decorated view
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split()[1]
        else:
            auth_token = ''

        if auth_token:
            resp = models.User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = models.User.query.filter_by(id=resp['user']).first()
                kwargs['user'] = user
                return func(*args, **kwargs)

            response = Response('Fail', resp)
            return make_response(jsonify(response._asdict())), 401

        else:
            response = Response('Fail', 'Provide a valid auth token')
            return make_response(jsonify(response._asdict())), 401

    return wrapper
