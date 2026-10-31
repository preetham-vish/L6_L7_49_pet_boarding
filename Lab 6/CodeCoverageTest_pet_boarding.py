import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status


# ---------- boarding_fee ----------
def test_within_included_days():
    assert boarding_fee("dog", 1, False) == 0

def test_unknown_pet_type():
    with pytest.raises(ValueError, match="unknown pet type"):
        boarding_fee("hamster", 1, False)

def test_negative_days():
    with pytest.raises(ValueError, match="invalid days"):
        boarding_fee("cat", -1, False)

def test_dog_extra_days_standard_rate():
    # included 2, 3 extra days * 30
    assert boarding_fee("dog", 5, False) == 90

def test_cat_premium_extra_days():
    # included 3 + 1 premium = 4, 2 extra * 20
    assert boarding_fee("cat", 6, True) == 40

def test_dog_long_stay_surcharge():
    # included 2, 12 extra * (30 + 10 + 5)
    assert boarding_fee("dog", 14, False) == 540

def test_cat_long_stay_surcharge():
    # included 3, 11 extra * (20 + 10)
    assert boarding_fee("cat", 14, False) == 330


# ---------- admission_ok ----------
def test_admission_ok():
    assert admission_ok(4, 2, False) is True

def test_admission_senior_enough_vaccinations():
    assert admission_ok(10, 3, True) is True

def test_admission_too_young():
    assert admission_ok(0, 5, False) is False


# ---------- checkout_status ----------
def test_checkout_open():
    assert checkout_status(20, False, False) == "open"

def test_checkout_late_long_stay_weekend():
    # cutoff 30 + 20 = 50, late window starts at 35
    assert checkout_status(40, True, True) == "late"

def test_checkout_closed():
    assert checkout_status(-1, False, False) == "closed"
