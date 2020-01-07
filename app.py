# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/HTTP/GET/', methods=['GET'])
@app.route('/api/HTTP/POST/', methods=['GET'])
@app.route('/api/HTTP/PUT/', methods=['GET'])
@app.route('/api/HTTP/DELETE/', methods=['GET'])
@app.route('/api/HTTP/INFO/', methods=['GET'])
@app.route('/api/HTTP/DUMB/', methods=['GET'])
def visit_url():
    url = request.values.get("url", None)
    method = request.url.split("/api/HTTP/")[1].split("/")[0]
    r = requests.request(method, url)

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
        "request_server": request_server
    }

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



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
