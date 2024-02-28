from http import HTTPStatus

from flask import jsonify

from . import app


class InvalidAPIUsage(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str, status_code: int = None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self) -> dict:
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error) -> tuple[str, int]:
    return jsonify(error.to_dict()), error.status_code
