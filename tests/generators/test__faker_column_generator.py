"""Tests that verify that data generation methods work as expected."""

import pytest
import random


from did_you_miss_me.generators.column import (
    FakerColumnGenerator,
)

@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)


#!!! Rename this
def test__generate_series_from_plan__column_missingness_type__always():
    generator = FakerColumnGenerator(
        name="test_column",
        faker_type="am_pm",
    )
    series = generator.generate(
        num_rows=20,
    )

    assert series.notnull().all()
    assert series.shape == (20,)
    print(series[:5].tolist())
    assert ("AM" in series.tolist()) or ("PM" in series.tolist())
