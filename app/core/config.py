from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = Field('sqlite:///db.sql')

settings = Settings()