from __future__ import annotations

import time
from collections import deque
from typing import Deque, Dict

from ..utils.exceptions import RateLimitExceeded


class RateLimiter:
	def __init__(self, limit_per_minute: int) -> None:
		self.limit = limit_per_minute
		self.window_seconds = 60
		self._hits: Dict[int, Deque[float]] = {}

	def check(self, user_id: int) -> None:
		now = time.time()
		q = self._hits.setdefault(user_id, deque())
		# очистим старые	since = now - self.window_seconds
		while q and q[0] < since:
			q.popleft()
		if len(q) >= self.limit:
			retry_after = int(q[0] + self.window_seconds - now) + 1
			raise RateLimitExceeded(retry_after)
		q.append(now)


