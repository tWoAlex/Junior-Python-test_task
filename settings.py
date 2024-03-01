import os
from pathlib import Path

import dotenv


dotenv.load_dotenv()

MEDIA_DIR: Path = Path(__file__).resolve().parent.joinpath(
    os.getenv('MEDIA_DIR', default='media')
)
FILE_SIZE_LIMIT: int = int(os.getenv('FILE_SIZE_LIMIT', default=1_048_576))
