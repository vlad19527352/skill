from __future__ import annotations

from functools import lru_cache
from pydantic import ValidationError
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


class Settings(BaseSettings):
	TELEGRAM_BOT_TOKEN: str = Field(..., min_length=10)
	PERPLEXITY_API_KEY: str = Field(..., min_length=10)
	PERPLEXITY_API_URL: str = Field(default="https://api.perplexity.ai/chat/completions")
	MODEL_NAME: str = Field(default="sonar")
	REQUEST_TIMEOUT_SECONDS: int = Field(default=20, ge=5, le=120)
	LOG_LEVEL: str = Field(default="INFO")
	RATE_LIMIT_PER_MINUTE: int = Field(default=20, ge=1, le=120)

	model_config = SettingsConfigDict(env_file=None, extra="ignore")


@lru_cache(maxsize=1)
def from_env() -> Settings:
	# Загружаем сначала .env, затем env (без точки), не перезаписывая уже установленные переменные
	load_dotenv(dotenv_path=".env", override=False)
	load_dotenv(dotenv_path="env", override=False)
	try:
		return Settings()  # type: ignore[call-arg]
	except ValidationError as exc:
		missing = ", ".join(err["loc"][0] for err in exc.errors())
		raise SystemExit(
			"Invalid configuration: отсутствуют или пустые переменные — " + missing +
			". Заполните их в .env (или env) и повторите."
		)


