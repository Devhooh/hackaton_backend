from flask import jsonify

def response(status_code: int, message, data=None, error=None, count_data=None):
    resp = {
        "statusCode": status_code,
        "message": message
    }
    if error is not None:
        resp["error"] = error
    if data is not None:
        resp["data"] = data
    if count_data is not None:
        resp["countData"] = count_data

    return jsonify(resp), status_code
