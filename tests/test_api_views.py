from http import HTTPStatus

from flask.testing import FlaskClient

from settings import FILE_SIZE_LIMIT
from .utils import random_base64_data, random_file_name


class TestAPIPostRequests:
    def test_file_create_empty_body(self, client: FlaskClient):
        response = client.post('/files/create/')

        assert 'error' in response.json
        assert response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    def test_file_create_without_name(self, client: FlaskClient):
        response = client.post('/files/create/', json={})
        data = response.json

        assert 'error' in data, 'response must have "error" key'
        assert 'file_name' in data['error'], ('response must message '
                                              '"file_name" not in request')
        assert 'missing' in data['error'], ('response must message '
                                            '"file_name" not in request')
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_file_create_without_data(self, client: FlaskClient):
        file_name = random_file_name()
        response = client.post('/files/create/', json={'file_name': file_name})
        data = response.json

        assert 'error' in data, 'response must have "error" key'
        assert file_name in data['error'], ('response must message about '
                                            'missing key made from file_name')
        assert 'missing' in data['error'], ('response must message that '
                                            'missing key made from file_name')
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_file_create_correct(self, client: FlaskClient):
        file_name = random_file_name()
        data = random_base64_data(FILE_SIZE_LIMIT)
        response = client.post(
            '/files/create/', json={'file_name': file_name, file_name: data}
        )
        assert response.status_code == HTTPStatus.CREATED

    def test_file_create_too_big_file(self, client: FlaskClient):
        file_name = random_file_name()
        data = random_base64_data(FILE_SIZE_LIMIT + 1)
        response = client.post(
            '/files/create/', json={'file_name': file_name, file_name: data}
        )
        assert 'error' in response.json, ('response must message about '
                                          'oversized file')
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_file_create_already_exist(self, client: FlaskClient):
        file_name = random_file_name()
        data = random_base64_data(FILE_SIZE_LIMIT)

        client.post('/files/create/',
                    json={'file_name': file_name, file_name: data})
        second_response = client.post(
            '/files/create/', json={'file_name': file_name, file_name: data}
        )

        correct_response_body_descr = ('response must message '
                                       'about same file exists')
        assert 'error' in second_response.json, correct_response_body_descr
        message = second_response.json['error'].lower()
        assert 'already' in message, correct_response_body_descr
        assert 'exist' in message, correct_response_body_descr
        assert second_response.status_code == HTTPStatus.BAD_REQUEST
