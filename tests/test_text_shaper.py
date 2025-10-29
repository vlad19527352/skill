from src.app.services.text_shaper import shape_to_window


def test_shape_short_text():
	text = "Короткий ответ."
	res = shape_to_window(text)
	assert res == text


def test_shape_soft_cut_sentence_boundary():
	text = ("Предложение один. Предложение два длительное и подробное, которое должно быть обрезано. "
			* 20)
	res = shape_to_window(text, min_len=500, max_len=700)
	assert 500 <= len(res) <= 700
	assert res.endswith(('.', '!', '?')) is True or len(res) == 700


def test_shape_hard_cut_when_needed():
	text = "слово" * 1000
	res = shape_to_window(text, min_len=500, max_len=700)
	assert 500 <= len(res) <= 700


