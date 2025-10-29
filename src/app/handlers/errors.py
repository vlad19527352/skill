from __future__ import annotations

import logging
from telegram import Update
from telegram.ext import Application, ContextTypes

from ..utils.exceptions import RateLimitExceeded


log = logging.getLogger(__name__)


def register_error_handlers(app: Application, rate_limiter) -> None:
	async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:  # type: ignore[override]
		log.exception("Unhandled error", exc_info=context.error)
		if isinstance(context.error, RateLimitExceeded):
			retry_after = context.error.retry_after_seconds
			if isinstance(update, Update) and update.effective_message:
				await update.effective_message.reply_text(
					f"Слишком много запросов. Попробуйте снова через ~{retry_after} сек."
				)
			return
		if isinstance(update, Update) and update.effective_message:
			await update.effective_message.reply_text(
				"Что-то пошло не так, но мы это исправим. Попробуйте ещё раз позже."
			)

	app.add_error_handler(on_error)


