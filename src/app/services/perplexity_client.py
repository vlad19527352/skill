from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import httpx
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from ..config import Settings
from ..utils.exceptions import ExternalServiceError


class PerplexityClient:
	def __init__(self, cfg: Settings) -> None:
		self._cfg = cfg
		self._client = httpx.AsyncClient(timeout=cfg.REQUEST_TIMEOUT_SECONDS)
		self._log = logging.getLogger(self.__class__.__name__)

	async def close(self) -> None:
		await self._client.aclose()

	async def ask(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> str:
		payload: Dict[str, Any] = {
			"model": model or self._cfg.MODEL_NAME,
			"messages": messages,
			"temperature": 0.2,
			"top_p": 0.9,
			"max_tokens": 900,
		}

		headers = {
			"Authorization": f"Bearer {self._cfg.PERPLEXITY_API_KEY}",
			"Content-Type": "application/json",
		}

		async for attempt in AsyncRetrying(
			stop=stop_after_attempt(3),
			wait=wait_exponential_jitter(initial=0.5, max=3.0),
			retry=retry_if_exception_type((httpx.TransportError, ExternalServiceError)),
		):
			with attempt:
				try:
					resp = await self._client.post(self._cfg.PERPLEXITY_API_URL, json=payload, headers=headers)
					if resp.status_code >= 500:
						raise ExternalServiceError(f"5xx from Perplexity: {resp.status_code}")
					resp.raise_for_status()
					data = resp.json()
					choices = data.get("choices") or []
					if not choices:
						return "К сожалению, я не получил содержательного ответа. Попробуйте ещё раз."
					message = choices[0].get("message", {})
					content = message.get("content") or ""
					return content.strip() or "К сожалению, я не получил содержательного ответа. Попробуйте ещё раз."
				except httpx.TimeoutException as exc:
					self._log.warning("Perplexity timeout", extra={"ctx_event": "perplexity_timeout"})
					raise ExternalServiceError("Timeout while contacting Perplexity") from exc


