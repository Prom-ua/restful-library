from functools import wraps

from flask import request
from flask.ext import restful

from restful_library.lib.utils import str_to_uuid
from restful_library.models.auth import ApiToken


def check_api_token(uuid):
    token = ApiToken.query.filter_by(uuid=uuid).first()
    if token and token.is_not_expired():
        return True
    return False


def token_authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if auth:
            uuid = str_to_uuid(auth.username)
            if uuid and check_api_token(uuid):
                return func(*args, **kwargs)

        restful.abort(401)
    return wrapper
