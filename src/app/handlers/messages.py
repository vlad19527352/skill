from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from .commands import post_command


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	# Переиспользуем логику /post
	await post_command(update, context)


