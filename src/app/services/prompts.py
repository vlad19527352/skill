from __future__ import annotations

from typing import List, Dict

SYSTEM_RU = (
    "Ты — активный и дружелюбный помощник. Отвечай кратко, по делу, "
    "в пределах до 800 символов. Пиши по-русски, избегай лишней воды."
)


def build_messages(user_text: str, language: str = "ru") -> List[Dict[str, str]]:
	messages: List[Dict[str, str]] = [
		{"role": "system", "content": SYSTEM_RU if language == "ru" else SYSTEM_RU},
		{"role": "user", "content": user_text},
	]
	return messages


