import base64

from settings import FILE_SIZE_LIMIT, MEDIA_DIR


MEDIA_DIR.mkdir(exist_ok=True)


class FileIsTooBig(MemoryError):
    """Exception for files bigger then specified FILE_SIZE_LIMIT"""

    def __init__(self, limit: int, *args) -> None:
        super().__init__(*args)
        self.limit = limit


class FileCRUD:
    """CRUD for files in media directory"""

    def all_files(self) -> list[str]:
        """List of file names in media directory"""

        return [file.name for file in MEDIA_DIR.glob('*.*')]

    def files_by_extension(self, extension: str) -> list[str]:
        """List of file names with specified extension"""

        return [file.name for file in MEDIA_DIR.glob(f'*.{extension}')]

    def exists(self, file_name: str) -> bool:
        """Checks if file exists"""

        return MEDIA_DIR.joinpath(file_name).exists()

    def create(self, file_name: str, data: str) -> None:
        """Creates local file from base64-encoded data"""

        data = base64.b64decode(data)
        if len(data) > FILE_SIZE_LIMIT:
            raise FileIsTooBig(limit=FILE_SIZE_LIMIT)
        with open(MEDIA_DIR.joinpath(file_name), 'wb') as file:
            file.write(data)

    def delete(self, file_name: str) -> bool:
        """Deletes file if exists"""

        MEDIA_DIR.joinpath(file_name).unlink(missing_ok=True)

    def get(self, file_name: str) -> str:
        """Returns base64-encoded data of requested file"""

        with open(MEDIA_DIR.joinpath(file_name), 'rb') as file:
            data = file.read()
        return bytes.decode(base64.b64encode(data))


file_crud = FileCRUD()
