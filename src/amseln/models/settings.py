from pydantic import BaseSettings


class Settings(BaseSettings):
    max_content_length: int
    max_comment_length: int
    mongo_db_url: str
    mongo_db_port: int

    class Config:
        env_file = "../../.env"
