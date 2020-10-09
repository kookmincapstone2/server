import functools

from flask import request
from werkzeug.exceptions import BadRequest

from db import Database


def api(f):
    @functools.wraps(f)
    def deco(*args, **kwargs):
        if request.method in ['GET', 'DELETE']:
            data = request.args.to_dict()
        elif request.method in ['POST', 'PUT']:
            data = request.form
        else:
            data = {}
        with Database() as db:
            return f(data, db, *args, **kwargs)

    return deco


def check_data(data, req_list):
    for i in req_list:
        if i not in data:
            raise BadRequest
