from __future__ import annotations

from .exceptions import InvalidInputError


def normalize_whitespace(text: str) -> str:
	return " ".join(text.split())


def validate_user_text(text: str, max_chars: int = 4000) -> str:
	clean = normalize_whitespace(text or "")
	if not clean:
		raise InvalidInputError("Пожалуйста, напишите вопрос после команды или в сообщении.")
	if len(clean) > max_chars:
		raise InvalidInputError("Слишком длинный запрос. Укоротите, пожалуйста.")
	return clean


