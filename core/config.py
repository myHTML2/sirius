from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Booking Service"
    DATABASE_URL: str = "postgresql://user:password@localhost/dbname"

    class Config:
        env_file = ".env"

settings = Settings()
