class ExternalServiceError(Exception):
	pass


class RateLimitExceeded(Exception):
	def __init__(self, retry_after_seconds: int) -> None:
		self.retry_after_seconds = retry_after_seconds
		super().__init__(f"Rate limit exceeded. Retry after {retry_after_seconds}s")


class InvalidInputError(ValueError):
	pass


