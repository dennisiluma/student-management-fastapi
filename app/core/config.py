from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # DATABASE
    DATABASE_URL: str

    # JWT VARIABELS
    SECRETE_JWT_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS:int



    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()


