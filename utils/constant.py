
from flask import Response, jsonify


def requestRespond(data, code, m="sucess"):
    resp = {
        "code": code,
        "message": m,
        "data": data,

    }
    return resp


def resquestErrorResponse(msg, cd=400) -> Response:
    resp = jsonify(requestRespond(
        m=msg,
        data=[], code=cd))
    resp.status_code = cd
    return resp
