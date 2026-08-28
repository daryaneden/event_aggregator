from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
     
    EVENT_PROVIDER_URL: str 
    EVENT_PROVIDER_API_KEY: str 
    DB_HOST: str = 'db'
    DB_PORT: int = 5432
    POSTGRES_USERNAME: str = 'postgres'
    POSTGRES_PASSWORD: str = 'password'
    DB_DRIVER: str = 'postgresql+asyncpg'
    DB_NAME: str = 'student_daryaneden-events-aggregator-postgres'


    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
