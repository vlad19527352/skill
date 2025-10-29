from __future__ import annotations

import re


def _soft_cut(text: str, max_len: int) -> str:
	if len(text) <= max_len:
		return text
	soft = text[:max_len]
	# Пытаемся закончить по границе предложения
	m = re.search(r"[\.!?]\s+\S*$", soft)
	if m:
		return soft[:m.end()].strip()
	# Потом по границе слова
	m2 = re.search(r"\s+\S*$", soft)
	if m2:
		return soft[:m2.start()].strip()
	# Жёсткая обрезка
	return soft.strip()


def shape_to_window(text: str, min_len: int = 600, max_len: int = 800) -> str:
	clean = text.strip()
	if len(clean) <= max_len:
		return clean
	res = _soft_cut(clean, max_len)
	if len(res) < min_len:
		# если после мягкого усечения слишком коротко — растянем до max_len
		res = clean[:max_len].rstrip()
	return res


def _remove_service_marks(text: str) -> str:
    # Удаляем типичные служебные пометки ссылок/сносок/источников
    patterns = [
        r"\[\d+\]",  # [1]
        r"\[\^\d+\]",  # [^1]
        r"\(Источник:[^)]*\)",  # (Источник: ...)
        r"\(Source:[^)]*\)",  # (Source: ...)
        r"^\s*(Ссылки|References)\s*:\s*.*$",  # строки со списком ссылок
    ]
    cleaned = text
    for p in patterns:
        cleaned = re.sub(p, "", cleaned, flags=re.IGNORECASE | re.MULTILINE)
    # Удаляем повторяющиеся пробелы и лишние пустые строки
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def _paragraphize(text: str, target_len: int = 800) -> str:
    # Делим на предложения и собираем абзацы по 2–4 предложения или ~300–400 символов
    sentences = re.split(r"(?<=[.!?])\s+", text)
    paragraphs = []
    current = []
    current_len = 0
    for s in sentences:
        if not s:
            continue
        current.append(s)
        current_len += len(s) + 1
        if len(current) >= 3 or current_len >= 360:
            paragraphs.append(" ".join(current).strip())
            current = []
            current_len = 0
    if current:
        paragraphs.append(" ".join(current).strip())
    # Добавляем эмодзи к началу каждого абзаца
    emojis = ["✨", "💡", "✅", "📌", "🔹", "🧠", "🚀"]
    decorated = []
    for idx, p in enumerate(paragraphs):
        emoji = emojis[idx % len(emojis)]
        decorated.append(f"{emoji} {p}")
    result = "\n\n".join(decorated)
    # На всякий случай поджимаем до целевого окна
    return _soft_cut(result, target_len)


def prettify_answer(text: str) -> str:
    no_marks = _remove_service_marks(text)
    return _paragraphize(no_marks, target_len=800)

