from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    EVENT_PROVIDER_URL = ''
    EVENT_PROVIDER_API_KEY = ''
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5433
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
    DB_DRIVER: str = 'postgresql+asyncpg'
    DB_NAME: str = ''

    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'