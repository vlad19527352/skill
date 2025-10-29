from __future__ import annotations

import logging
import sys
import time
from typing import Any, Dict

import orjson


class OrjsonFormatter(logging.Formatter):
	def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
		payload: Dict[str, Any] = {
			"ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(record.created)),
			"level": record.levelname,
			"logger": record.name,
			"message": record.getMessage(),
		}
		if record.exc_info:
			payload["exc_info"] = self.formatException(record.exc_info)
		for key, value in getattr(record, "__dict__", {}).items():
			if key.startswith("ctx_"):
				payload[key] = value
		return orjson.dumps(payload).decode("utf-8")


def setup_logging(level: str = "INFO") -> None:
	root = logging.getLogger()
	root.setLevel(level.upper())
	for h in list(root.handlers):
		root.removeHandler(h)
	stream = logging.StreamHandler(sys.stdout)
	stream.setLevel(level.upper())
	stream.setFormatter(OrjsonFormatter())
	root.addHandler(stream)


