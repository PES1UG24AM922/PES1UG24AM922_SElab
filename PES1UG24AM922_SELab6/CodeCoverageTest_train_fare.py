
import pytest

from train_fare import base_fare, concession, tatkal_charge


def test_base_fare_valid_sleeper():
    assert base_fare("SL", 500) == 500


def test_base_fare_minimum_fare():
    assert base_fare("3A", 10) == 50


def test_base_fare_unknown_class():
    with pytest.raises(ValueError, match="unknown class"):
        base_fare("CC", 100)


def test_base_fare_invalid_distance():
    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("SL", 0)


def test_concession_adult():
    assert concession(30, "M", False) == 0


def test_concession_child_below_five():
    assert concession(4, "F", False) == 100


def test_concession_child_up_to_twelve():
    assert concession(10, "M", False) == 50


def test_concession_senior_female():
    assert concession(65, "F", False) == 50


def test_concession_tatkal():
    assert concession(65, "M", True) == 0


def test_tatkal_sleeper_minimum_charge():
    assert tatkal_charge("SL", 500) == 100


def test_tatkal_other_class_normal_charge():
    assert tatkal_charge("3A", 1000) == 300


def test_tatkal_other_class_maximum_charge():
    assert tatkal_charge("2A", 2000) == 400

