from pathlib import Path

from pydantic import BaseSettings

ROOT_PATH = Path(__file__).parent.parent.parent.parent.absolute()


class Settings(BaseSettings):
    max_content_length: int
    max_comment_length: int
    mongo_db_url: str
    mongo_db_port: int
    root_path: str = str(ROOT_PATH)

    class Config:
        env_file = f"{ROOT_PATH}/.env"
