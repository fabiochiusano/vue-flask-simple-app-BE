# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
heroku = Heroku(app)
db = SQLAlchemy(app)

import models

@app.route('/api/HTTP/GET/', methods=['GET'])
@app.route('/api/HTTP/POST/', methods=['GET'])
@app.route('/api/HTTP/PUT/', methods=['GET'])
@app.route('/api/HTTP/DELETE/', methods=['GET'])
@app.route('/api/HTTP/INFO/', methods=['GET'])
@app.route('/api/HTTP/DUMB/', methods=['GET'])
def visit_url():
    errors = {}
    try:
        url = request.values.get("url", None)
        method = request.url.split("/api/HTTP/")[1].split("/")[0]
        r = requests.request(method, url)
    except Exception as e:
        errors["on_request"] = str(e)

    http_version = r.raw.version
    http_version_string = "HTTP/" + ".".join(str(http_version))
    status_code = r.status_code
    reason = r.reason
    request_date = " ".join(r.headers["Date"].split(" ")[:4])
    request_server = r.headers["Server"]

    resp = {
        "http_version_string": http_version_string,
        "status_code": status_code,
        "reason": reason,
        "request_date": request_date,
        "request_server": request_server,
        "id": ""
    }

    try:
        respRow = models.Response(**resp)
        db.session.add(respRow)
        db.session.commit()
        resp["id"] = respRow.id
    except Exception as e:
	    errors["on_db_add"] = str(e)

    req = {
        "method": method,
        "url": url
    }

    print(url, method)
    print(request.url)

    response = {
        "status": r.status_code,
        "errors": {},
        "data": {
            "url": url,
            "response": resp,
            "request": req
        }
    }

    # Return the response in json format
    return jsonify(response)

@app.route('/<path:request_id>', methods=['GET'])
def check_resourse(request_id):
    print(request_id)

    response = {
        "request_id": request_id
    }

    return jsonify(response)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
