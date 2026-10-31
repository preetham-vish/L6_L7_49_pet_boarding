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

def test_zero_days_is_valid_and_free():
    # days == 0 -> not negative (False branch of days < 0)
    assert boarding_fee("cat", 0, False) == 0

def test_extra_exactly_zero_is_free():
    # boundary: extra == 0 -> still "extra <= 0"
    assert boarding_fee("dog", 2, False) == 0

def test_premium_dog_gets_extra_day():
    # included 2 + 1 = 3; 4 days -> 1 extra * 30
    assert boarding_fee("dog", 4, True) == 30

def test_premium_rabbit_gets_no_extra_day():
    # is_premium True but pet is rabbit -> included stays 4; 5 days -> 1 * 20
    assert boarding_fee("rabbit", 5, True) == 20

def test_non_premium_cat_no_extra_day():
    # is_premium False short-circuits the condition
    assert boarding_fee("cat", 4, False) == 20

def test_dog_standard_rate():
    assert boarding_fee("dog", 5, False) == 90

def test_cat_standard_rate():
    assert boarding_fee("cat", 5, False) == 40

def test_extra_exactly_ten_has_no_surcharge():
    # boundary: extra == 10 -> "extra > 10" False; cat 13 days -> 10 * 20
    assert boarding_fee("cat", 13, False) == 200

def test_dog_long_stay_surcharge():
    # extra 11 -> rate 30 + 10 + 5
    assert boarding_fee("dog", 13, False) == 11 * 45

def test_cat_long_stay_surcharge():
    # extra 11 -> rate 20 + 10 (inner dog check False)
    assert boarding_fee("cat", 14, False) == 11 * 30


# ---------- admission_ok ----------
def test_admission_ok():
    assert admission_ok(4, 2, False) is True

def test_admission_senior_pass():
    assert admission_ok(10, 3, True) is True

def test_admission_senior_fail():
    assert admission_ok(10, 2, True) is False

def test_admission_too_young():
    assert admission_ok(0, 5, False) is False

def test_admission_adult_not_enough_vaccinations():
    assert admission_ok(4, 1, False) is False


# ---------- checkout_status ----------
def test_checkout_open_short_stay_weekday():
    assert checkout_status(15, False, False) == "open"

def test_checkout_late_boundary():
    # cutoff 15 -> late when 0 <= minutes < 15
    assert checkout_status(0, False, False) == "late"

def test_checkout_closed():
    assert checkout_status(-1, False, False) == "closed"

def test_checkout_long_stay_weekend():
    # cutoff 30 + 20 = 50
    assert checkout_status(50, True, True) == "open"
    assert checkout_status(35, True, True) == "late"
    assert checkout_status(34, True, True) == "closed"

def test_checkout_long_stay_weekday():
    assert checkout_status(30, True, False) == "open"

def test_checkout_short_stay_weekend():
    # cutoff 15 + 20 = 35
    assert checkout_status(35, False, True) == "open"
