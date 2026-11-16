import pytest
from src.phone import normalize_kz_phone


@pytest.mark.parametrize("raw", ["8 701 123 45 67"])
def test_normalize_kz_phone_raw(raw):
    assert normalize_kz_phone(raw) == "+77011234567"
