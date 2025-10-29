from __future__ import annotations

import time
from collections import defaultdict
from typing import Dict


class Metrics:
	def __init__(self) -> None:
		self.counters: Dict[str, int] = defaultdict(int)

	def inc(self, name: str) -> None:
		self.counters[name] += 1

	def get(self, name: str) -> int:
		return self.counters.get(name, 0)


