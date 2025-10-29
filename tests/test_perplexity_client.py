import asyncio
from typing import Any

import httpx
import pytest

from src.app.config import Settings
from src.app.services.perplexity_client import PerplexityClient


class DummySettings(Settings):
	TELEGRAM_BOT_TOKEN: str = "x" * 32
	PERPLEXITY_API_KEY: str = "y" * 32


def make_client(monkeypatch, status_code: int, json_data: dict[str, Any]):
	cfg = DummySettings()
	client = PerplexityClient(cfg)

	class DummyResponse:
		def __init__(self, status_code: int, data: dict[str, Any]):
			self.status_code = status_code
			self._data = data

		def json(self):
			return self._data

		def raise_for_status(self):
			if self.status_code >= 400 and self.status_code < 500:
				raise httpx.HTTPStatusError("client error", request=None, response=None)

	async def fake_post(url, json, headers):
		return DummyResponse(status_code, json_data)  # type: ignore[return-value]

	monkeypatch.setattr(client._client, "post", fake_post)
	return client


@pytest.mark.asyncio
async def test_ask_success(monkeypatch):
	client = make_client(monkeypatch, 200, {"choices": [{"message": {"content": "привет"}}]})
	res = await client.ask([{"role": "user", "content": "hi"}], model="sonar")
	assert res == "привет"
	await client.close()


@pytest.mark.asyncio
async def test_ask_empty_choices(monkeypatch):
	client = make_client(monkeypatch, 200, {"choices": []})
	res = await client.ask([{"role": "user", "content": "hi"}], model="sonar")
	assert "не получил" in res
	await client.close()


