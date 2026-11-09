import pytest
from src.phone import normalize_kz_phone


def test_normalize_kz_phone_starts_with_eight():
    """8-ден басталатын және бос орындары бар нөмірді қалыпқа келтіру."""
    assert normalize_kz_phone("8 701 123 45 67") == "+77011234567"


def test_normalize_kz_phone_formatted_with_brackets():
    """+7 коды бар, жақша және сызықшалармен жазылған нөмірді тексеру."""
    assert normalize_kz_phone("+7 (777) 987-65-43") == "+77779876543"


def test_normalize_kz_phone_short_number_raises_value_error():
    """Қысқа (жарамсыз) нөмір берілгенде ValueError лақтырылуын тексеру."""
    with pytest.raises(ValueError, match="ұзындығы дұрыс емес"):
        normalize_kz_phone("12345")


def test_normalize_kz_phone_invalid_characters_raises_value_error():
    """Әріп немесе бөтен таңбалар кездескенде ValueError лақтырылуын тексеру."""
    with pytest.raises(ValueError, match="жарамсыз таңбалар бар"):
        normalize_kz_phone("8 701 ABC 45 67")

