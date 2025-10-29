from __future__ import annotations

import logging
from telegram import Update
from telegram.ext import ContextTypes

from ..services.perplexity_client import PerplexityClient
from ..services.prompts import build_messages
from ..services.text_shaper import shape_to_window, prettify_answer
from ..utils.tracing import generate_request_id
from ..utils.validators import validate_user_text


log = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	await update.message.reply_text(
		"Привет! Я дружелюбный бот с доступом к Perplexity. Задайте вопрос командой /post или просто сообщением. 😊"
	)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	await update.message.reply_text(
		"Подсказка: используйте /post <вопрос> или отправьте текст. "
		"Ответы 500–700 символов. Пишите по теме, я отвечу кратко и по делу!"
	)


async def post_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	request_id = generate_request_id()
	user_text_raw = (update.message.text or "").replace("/post", "", 1).strip()
	try:
		user_text = validate_user_text(user_text_raw)
	except Exception as exc:
		await update.message.reply_text(str(exc))
		return

	client: PerplexityClient = context.bot_data.get("perplexity_client")
	if client is None:
		# Инициализируем клиент отложенно (на случай перезапуска)
		from ..config import from_env
		from ..services.perplexity_client import PerplexityClient as _PC
		cfg = from_env()
		client = _PC(cfg)
		context.bot_data["perplexity_client"] = client

	messages = build_messages(user_text)
	try:
		answer = await client.ask(messages)
		answer = shape_to_window(answer)
		answer = prettify_answer(answer)
		await update.message.reply_text(answer)
	except Exception as exc:
		log.exception("post_command failed", extra={"ctx_request_id": request_id})
		await update.message.reply_text(
			"Ой, возникла временная сложность при обращении к Perplexity. Попробуем ещё раз чуть позже?"
		)


