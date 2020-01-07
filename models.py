from app import db

class Response(db.Model):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    http_version_string = db.Column(db.String())
    status_code = db.Column(db.Integer)
    reason = db.Column(db.String())
    request_date = db.Column(db.String())
    request_server = db.Column(db.String())

    def __init__(self, http_version_string, status_code, reason,
                request_date, request_server):
        self.http_version_string = http_version_string
        self.status_code = status_code
        self.reason = reason
        self.request_date = request_date
        self.request_server = request_server

    def serialize(self):
        return {
            'id': self.id,
            'http_version_string': self.http_version_string,
            'status_code': self.status_code,
            'reason': self.reason,
            'request_date': self.request_date,
            'request_server': self.request_server
        }
