import pytest
from hypothesis import given, strategies as st
from pet_boarding import parse_booking, stay_average, payable_fee


# ---------- parse_booking ----------

@given(
    pet=st.sampled_from(["dog", "cat", "rabbit"]),
    days=st.floats(min_value=0, max_value=365,
                   allow_nan=False, allow_infinity=False)
)
def test_parse_booking_valid(pet, days):
    result = parse_booking(f"{pet}:{days}")
    assert result[0] == pet.title()
    assert result[1] == days


@given(s=st.text())
def test_parse_booking_arbitrary_input(s):
    try:
        result = parse_booking(s)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result[0] in ["Dog", "Cat", "Rabbit"]
        assert result[1] >= 0
    except (ValueError, TypeError):
        pass


@pytest.mark.parametrize("s", [
    "", "dog", "dog:5:extra", ":5",
    "hamster:3", "dog:-5", "dog:abc",
    "dog:nan", "dog:inf"
])
def test_parse_booking_invalid(s):
    with pytest.raises(ValueError):
        parse_booking(s)


# ---------- stay_average ----------

@given(
    days=st.lists(
        st.integers(min_value=0, max_value=365),
        min_size=1,
        max_size=50
    )
)
def test_stay_average_valid(days):
    csv = ",".join(map(str, days))
    expected = sum(days) // len(days)
    assert stay_average(csv) == expected


@given(s=st.text())
def test_stay_average_arbitrary_input(s):
    try:
        result = stay_average(s)
        assert isinstance(result, int)
        assert result >= 0
    except (ValueError, TypeError):
        pass


@pytest.mark.parametrize("s", [
    "", "1,,2", "1,abc,3", "-1,2",
    "1,2,", ",1,2", "1.5,2"
])
def test_stay_average_invalid(s):
    with pytest.raises(ValueError):
        stay_average(s)


# ---------- payable_fee ----------

@given(
    fee=st.floats(min_value=0, max_value=100000,
                  allow_nan=False, allow_infinity=False),
    discount=st.floats(min_value=0, max_value=100000,
                       allow_nan=False, allow_infinity=False)
)
def test_payable_fee_valid(fee, discount):
    result = payable_fee(f"{fee}|{discount}")
    expected = max(fee * 1.18 - discount, 0)
    assert result == pytest.approx(expected)


@given(s=st.text())
def test_payable_fee_arbitrary_input(s):
    try:
        result = payable_fee(s)
        assert isinstance(result, (int, float))
        assert result >= 0
    except (ValueError, TypeError):
        pass


@pytest.mark.parametrize("s", [
    "", "100", "100|20|5", "|20",
    "100|abc", "abc|20", "-100|20",
    "100|-20", "nan|10", "inf|10"
])
def test_payable_fee_invalid(s):
    with pytest.raises(ValueError):
        payable_fee(s)
