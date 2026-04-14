from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "llm-p"
    env: str = "local"

    jwt_secret: str = "change_me_super_secret"
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 60

    sqlite_path: str = "./app.db"

    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "nvidia/nemotron-nano-9b-v2:free"
    openrouter_site_url: str = "https://example.com"
    openrouter_app_name: str = "llm-fastapi-openrouter"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
