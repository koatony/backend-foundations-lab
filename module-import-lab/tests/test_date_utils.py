import pytest

from app.date_utils import calculate_days_between, show_name
@pytest.mark.parametrize(("date1_str","date2_str","expected_days"), [
    ("2026-07-20", "2026-07-25",5),
    ("2026-07-25", "2026-07-20",5),
    ("2026-07-25", "2026-07-25",0),
    ("2024-02-28", "2024-03-01",2)
])

def test_calculate_days_between(date1_str, date2_str, expected_days)->None:
    assert calculate_days_between(date1_str, date2_str) == expected_days
    


def test_rejects_invalid_date()->None:
    with pytest.raises(ValueError):
        calculate_days_between("invalid", "2026-06-07")


def test_rejects_imposible_date()->None:
    with pytest.raises(ValueError):
        calculate_days_between("2026-02-30","2026-07-20")

