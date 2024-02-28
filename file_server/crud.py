import base64

from settings import MEDIA_DIR


MEDIA_DIR.mkdir(exist_ok=True)


class FileCRUD:
    def all_files(self) -> list[str]:
        return [file.name for file in MEDIA_DIR.glob('*.*')]

    def files_by_extension(self, ext: str) -> list[str]:
        return [file.name for file in MEDIA_DIR.glob(f'*.{ext}')]

    def exists(self, file_name: str) -> bool:
        return MEDIA_DIR.joinpath(file_name).exists()

    def create(self, file_name: str, data: str) -> None:
        """Creates local file from base64-encoded data"""
        data = base64.b64decode(data)
        with open(MEDIA_DIR.joinpath(file_name), 'wb') as file:
            file.write(data)

    def delete(self, file_name: str) -> bool:
        MEDIA_DIR.joinpath(file_name).unlink(missing_ok=True)

    def get(self, file_name: str) -> str:
        """Returns base64-encoded data"""
        with open(MEDIA_DIR.joinpath(file_name), 'rb') as file:
            data = file.read()
        return bytes.decode(base64.b64encode(data))


file_crud = FileCRUD()
