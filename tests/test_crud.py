from random import randint

from file_server.crud import MEDIA_DIR, file_crud
from settings import FILE_SIZE_LIMIT

from .utils import (random_base64_data,
                    random_file_extension,
                    random_file_name,
                    random_file_prefix)


class TestCRUDCreate:
    def test_file_create(self, app):
        file_name = random_file_name()
        data = random_base64_data(FILE_SIZE_LIMIT)
        file_crud.create(file_name, data)

        assert MEDIA_DIR.joinpath(file_name).exists(), (
            'File have not been created'
        )


class TestCRUDGet:
    def test_file_retrieve(self, app):
        file_name = random_file_name()
        data = random_base64_data(FILE_SIZE_LIMIT)
        file_crud.create(file_name, data)

        data_from_crud = file_crud.get(file_name)
        assert data == data_from_crud, (
            'File data from CRUD is broken'
        )


class TestCRUDList:
    def test_file_list(self, app):
        files = ((random_file_name(), random_base64_data(FILE_SIZE_LIMIT))
                 for _ in range(randint(3, 10)))
        for file_name, data in files:
            file_crud.create(file_name, data)

        file_list = file_crud.all_files()
        for file_name, data in files:
            assert file_name in file_list, ('Created file is missing')

    def test_file_extension_filter(self, app):
        ext = random_file_extension()
        files = (
            (f'{random_file_prefix()}.{ext}',
             random_base64_data(FILE_SIZE_LIMIT))
            for _ in range(randint(3, 10))
        )
        another_file_name = f'{random_file_prefix()}.{ext + "abc"}'
        another_file_data = random_base64_data(FILE_SIZE_LIMIT)

        for file_name, data in files:
            file_crud.create(file_name, data)
        file_crud.create(another_file_name, another_file_data)

        ext_filtered_list = file_crud.files_by_extension(ext)
        assert another_file_name not in ext_filtered_list, (
            'By-extension filter is broken'
        )
        for file_name, data in files:
            assert file_name in ext_filtered_list, (
                'By-extension filter missed file'
            )


class TestCRUDDelete:
    def test_file_delete(self, app):
        file_name = random_file_name()
        data = random_base64_data(FILE_SIZE_LIMIT)
        file_crud.create(file_name, data)

        file_crud.delete(file_name)
        assert not MEDIA_DIR.joinpath(file_name).exists(), (
            'File has not been actually deleted'
        )
