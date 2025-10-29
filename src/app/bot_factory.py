from __future__ import annotations

import logging
from typing import Callable

from telegram.ext import (Application, ApplicationBuilder, CommandHandler,
                          MessageHandler, filters)

from .config import Settings
from .handlers.commands import help_command, post_command, start_command
from .handlers.errors import register_error_handlers
from .handlers.messages import handle_text_message
from .middlewares.rate_limit import RateLimiter
from .middlewares.metrics import Metrics


def create_application(cfg: Settings) -> Application:
	app: Application = (
		ApplicationBuilder()
		.token(cfg.TELEGRAM_BOT_TOKEN)
		.build()
	)

	# Middlewares (простые, на уровне обработчиков)
	rate_limiter = RateLimiter(limit_per_minute=cfg.RATE_LIMIT_PER_MINUTE)
	metrics = Metrics()

	# Команды
	app.add_handler(CommandHandler("start", start_command))
	app.add_handler(CommandHandler("help", help_command))
	app.add_handler(CommandHandler("post", post_command))

	# Сообщения
	app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

	# Ошибки
	register_error_handlers(app, rate_limiter)

	# Храним ссылки на middleware в bot_data
	app.bot_data["rate_limiter"] = rate_limiter
	app.bot_data["metrics"] = metrics

	logging.getLogger(__name__).info("Application created")
	return app


