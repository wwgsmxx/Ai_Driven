import pytest
form src.phone import normalize_kz_phone

@pytest.mark.parametrize("raw", ["8 701 123 45 67"])