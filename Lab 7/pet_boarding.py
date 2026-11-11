import math

VALID_PETS = {"dog", "cat", "rabbit"}
def parse_booking(text):
    if not isinstance(text, str):
        raise TypeError("booking must be a string")

    parts = text.split(":")

    if len(parts) != 2:
        raise ValueError("invalid booking format")

    pet, days = parts
    pet = pet.strip().lower()

    if pet not in VALID_PETS:
        raise ValueError("unknown pet type")

    try:
        days = float(days)
    except ValueError:
        raise ValueError("invalid boarding days")

    if not math.isfinite(days) or days < 0:
        raise ValueError("invalid boarding days")

    return pet.title(), days


def stay_average(days_csv):
    if not isinstance(days_csv, str):
        raise TypeError("stay lengths must be a string")

    if not days_csv.strip():
        raise ValueError("stay lengths cannot be empty")

    try:
        values = [int(r.strip()) for r in days_csv.split(",")]
    except ValueError:
        raise ValueError("invalid stay length")

    if any(value < 0 for value in values):
        raise ValueError("stay lengths cannot be negative")

    return sum(values) // len(values)


def payable_fee(text):
    if not isinstance(text, str):
        raise TypeError("fee information must be a string")

    parts = text.split("|")

    if len(parts) != 2:
        raise ValueError("invalid fee format")

    try:
        fee = float(parts[0])
        discount = float(parts[1])
    except ValueError:
        raise ValueError("fee and discount must be numeric")

    if not math.isfinite(fee) or not math.isfinite(discount):
        raise ValueError("fee and discount must be finite")

    if fee < 0 or discount < 0:
        raise ValueError("fee and discount cannot be negative")

    total = fee * 1.18 - discount

    return max(total, 0)


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter pet:days (e.g. dog:5): ")
    result = parse_booking(user_input)
    print("Pet and Days:", result)

    print("\n==== Running stay_average ====")
    user_input = input("Enter stay lengths in days as CSV (e.g. 2,5,7): ")
    result = stay_average(user_input)
    print("Average Stay:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 1500|100): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)


if __name__ == "__main__":
    main()
