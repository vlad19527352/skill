from __future__ import annotations

import logging
import platform

if platform.system() != "Windows":
	try:
		import uvloop  # type: ignore
		uvloop.install()
	except Exception:
		pass

from .bot_factory import create_application
from .config import from_env
from .logging_config import setup_logging
from .services.perplexity_client import PerplexityClient


def main() -> None:
	cfg = from_env()
	setup_logging(cfg.LOG_LEVEL)
	log = logging.getLogger("app")
	log.info("Starting bot")

	app = create_application(cfg)
	# Готовим Perplexity клиента заранее и кладём в bot_data
	app.bot_data["perplexity_client"] = PerplexityClient(cfg)

	# Блокирующий запуск polling
	app.run_polling(allowed_updates=None)


if __name__ == "__main__":
	main()
