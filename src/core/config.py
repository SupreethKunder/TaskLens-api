from pydantic_settings import BaseSettings, SettingsConfigDict
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Monitoring APIs"
    API_VERSION: str = "0.0.0"
    BASE_URL: str = "0.0.0.0"
    REDIS_URL: str
    TEST_LOGIN: str
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_JWT: str
    SUPABASE_BUCKET: str

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )


settings = Settings()
