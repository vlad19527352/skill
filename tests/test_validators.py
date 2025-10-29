import pytest

from src.app.utils.validators import normalize_whitespace, validate_user_text
from src.app.utils.exceptions import InvalidInputError


def test_normalize_whitespace():
	assert normalize_whitespace("  a\t b\n c  ") == "a b c"


def test_validate_user_text_ok():
	assert validate_user_text("  вопрос  ") == "вопрос"


def test_validate_user_text_empty():
	with pytest.raises(InvalidInputError):
		validate_user_text("   ")


def test_validate_user_text_too_long():
	with pytest.raises(InvalidInputError):
		validate_user_text("a" * 5001, max_chars=5000)


