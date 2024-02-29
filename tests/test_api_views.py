from http import HTTPStatus
from random import randint

from flask.testing import FlaskClient

from settings import FILE_SIZE_LIMIT
from .utils import (random_base64_data,
                    random_file_extension,
                    random_file_name,
                    random_file_prefix)


class TestAPICreate:
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


class TestAPIList:
    def test_file_list(self, client: FlaskClient):
        files = ((random_file_name(), random_base64_data(FILE_SIZE_LIMIT))
                 for _ in range(randint(3, 10)))
        for name, data in files:
            client.post('/files/create/',
                        json={'file_name': name, name: data})
        response = client.get('/files/get/list')

        for name, data in files:
            assert name in response.json, f'File "{name}" is missing'
        assert response.status_code == HTTPStatus.OK

    def test_file_list_by_ext(self, client: FlaskClient):
        ext = random_file_extension()
        files = (
            (f'{random_file_prefix()}.{ext}',
             random_base64_data(FILE_SIZE_LIMIT))
            for _ in range(randint(3, 10))
        )
        another_file_name = f'{random_file_prefix()}.{ext + "abc"}'
        another_file_data = random_base64_data(FILE_SIZE_LIMIT)
        for name, data in files:
            client.post('/files/create/',
                        json={'file_name': name, name: data})
        client.post('/files/create/',
                    json={'file_name': another_file_name,
                          another_file_name: another_file_data})
        response = client.get(f'/files/get/{ext}')

        assert another_file_name not in response.json, ('Extension filter'
                                                        ' is broken')
        for name, data in files:
            assert name in response.json, ('File "{name}" from extension-'
                                           'filtered list is missing')
        assert response.status_code == HTTPStatus.OK


class TestAPIGet:
    def test_get_uploaded_file(self, client: FlaskClient):
        prefix, ext = random_file_prefix(), random_file_extension()
        file_name = f'{prefix}.{ext}'
        data = random_base64_data(FILE_SIZE_LIMIT)
        client.post('/files/create/',
                    json={'file_name': file_name, file_name: data})
        response = client.get(f'/files/get/{ext}/{prefix}')

        assert 'file_name' in response.json, '"file_name" key is missing'
        assert response.json['file_name'] in response.json, ('File name as'
                                                             ' key is missing')
        assert response.json['file_name'] == file_name, ('File name in '
                                                         'response is broken')
        assert response.json[file_name] == data, ('File data in response'
                                                  ' is broken')
        assert response.status_code == HTTPStatus.OK


class TestAPIDelete:
    def test_delete_existing_file(self, client: FlaskClient):
        file_name = random_file_name()
        data = random_base64_data(FILE_SIZE_LIMIT)
        client.post('/files/create/',
                    json={'file_name': file_name, file_name: data})
        response = client.delete(f'/files/delete/{file_name}')

        assert response.status_code == HTTPStatus.NO_CONTENT
