from http import HTTPStatus

from flask import request
from werkzeug.exceptions import UnsupportedMediaType

from . import app
from .crud import FileIsTooBig, file_crud
from .error_handlers import InvalidAPIUsage


file_not_found = InvalidAPIUsage('File does not exist', HTTPStatus.NOT_FOUND)


@app.get('/files/get/list')
def list_files() -> tuple[list[str], int]:
    """Returns list of all available files"""

    return file_crud.all_files()


@app.get('/files/get/<string:extension>')
def list_files_by_extension(extension: str) -> tuple[list[str], int]:
    """Returns list of all available files with specified extension"""

    return file_crud.files_by_extension(extension)


@app.get('/files/get/<string:extension>/<string:file_name>')
def get_file(extension: str, file_name: str) -> tuple[dict[str, str], int]:
    """Returns file with name as <file_name>.<extension> as dict {
        "file_name": <file name>,
        <file name>" <base64 encoded file data>
    }"""

    file_name = f'{file_name}.{extension}'
    if not file_crud.exists(file_name):
        raise file_not_found
    return {'file_name': file_name,
            file_name: file_crud.get(file_name)}


@app.delete('/files/delete/<string:file_name>')
def delete_file(file_name: str) -> tuple[dict[str, str], int]:
    """Deletes file with specified file name"""

    if not file_crud.exists(file_name):
        raise file_not_found
    file_crud.delete(file_name)
    return {'message': 'deleted'}, HTTPStatus.NO_CONTENT


@app.post('/files/create/')
def create_file() -> tuple[dict[str, str], int]:
    """Creates file from dict {
        "file_name": <file name>,
        <file name>: <base64 encoded file data>
    }"""

    try:
        data = request.get_json()
    except UnsupportedMediaType:
        raise InvalidAPIUsage('Your request must contain JSON data',
                              HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    if data is None:
        raise InvalidAPIUsage('Request body is empty')

    file_name = data.get('file_name', None)
    if file_name is None:
        raise InvalidAPIUsage('"file_name" key is missing')
    if file_crud.exists(file_name):
        raise InvalidAPIUsage('File already exist')

    data = data.get(file_name, None)
    if data is None:
        raise InvalidAPIUsage(f'"{file_name}" key is missing')

    try:
        file_crud.create(file_name, data)
    except FileIsTooBig as exc:
        raise InvalidAPIUsage('File size exceeds maximum of'
                              f' {exc.limit} bytes')

    return {'message': 'created'}, HTTPStatus.CREATED
