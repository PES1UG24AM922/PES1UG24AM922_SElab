
import pytest
from hypothesis import given, strategies as st, example

from train_fare import parse_pnr, journey_distance, berth_type, BERTHS


@given(st.text() | st.none())
@example(None)
def test_parse_pnr_no_crash(s):
    valid = (
        isinstance(s, str)
        and len(s.strip()) == 10
        and s.strip().isascii()
        and s.strip().isdigit()
    )

    if valid:
        pnr = s.strip()
        assert parse_pnr(s) == (int(pnr[0]), int(pnr[1:]))
    else:
        with pytest.raises(ValueError):
            parse_pnr(s)


@given(st.text() | st.none())
@example(None)
def test_journey_distance_no_crash(s):
    valid = False

    if isinstance(s, str):
        parts = [part.strip() for part in s.split(",")]

        if (
            len(parts) >= 2
            and all(part and part.isascii() and part.isdigit() for part in parts)
        ):
            distances = [int(part) for part in parts]
            valid = all(
                distances[i] <= distances[i + 1]
                for i in range(len(distances) - 1)
            )

    if valid:
        assert journey_distance(s) == distances[-1] - distances[0]
    else:
        with pytest.raises(ValueError):
            journey_distance(s)


@given(st.text() | st.none())
@example(None)
def test_berth_type_no_crash(s):
    valid = False

    if isinstance(s, str):
        parts = s.strip().split("-")

        if len(parts) == 2:
            coach, number = parts[0].strip(), parts[1].strip()

            valid = (
                bool(coach)
                and coach.isascii()
                and coach[0].isalpha()
                and coach.isalnum()
                and bool(number)
                and number.isascii()
                and number.isdigit()
                and int(number) >= 1
            )

    if valid:
        assert berth_type(s) == (
            coach.upper(),
            BERTHS[int(number) % len(BERTHS)]
        )
    else:
        with pytest.raises(ValueError):
            berth_type(s)


@given(st.text(alphabet="0123456789", min_size=10, max_size=10))
def test_parse_pnr_valid_inputs(pnr):
    assert parse_pnr(pnr) == (int(pnr[0]), int(pnr[1:]))


@given(st.lists(st.integers(min_value=0, max_value=1000000),
                min_size=2, max_size=20))
def test_journey_distance_valid_inputs(values):
    values.sort()
    csv = ",".join(map(str, values))
    assert journey_distance(csv) == values[-1] - values[0]


@given(st.integers(min_value=1, max_value=10000))
def test_berth_type_valid_inputs(seat_number):
    assert berth_type(f"S3-{seat_number}") == (
        "S3",
        BERTHS[seat_number % len(BERTHS)]
    )

