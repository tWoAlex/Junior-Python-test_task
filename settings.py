import os
from pathlib import Path

import dotenv


dotenv.load_dotenv()

MEDIA_DIR = Path(__file__).resolve().parent.joinpath(
    os.getenv('MEDIA_DIR', default='media')
)
FILE_SIZE_LIMIT = 1024 * 1024
