
from flask import Response, jsonify
import constant


def requestRespond(data, code, m="message"):
    resp = {
        "code": code,
        m: data,

    }
    return resp


def resquestErrorResponse(msg, cd=400) -> Response:
    resp = jsonify(constant.requestRespond(
        m="data",
        data=[], code=cd))
    resp.status_code = cd
    return resp
