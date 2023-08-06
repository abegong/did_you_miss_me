"""Tests that verify that data generation methods work as expected."""

import pytest
import random


from did_you_miss_me.plans import (
    ColumnGenerationPlan,
)
from did_you_miss_me.series_generators import (
    generate_series_from_plan,
)


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)


def test__generate_series_from_plan__column_missingness_type__always():
    plan = ColumnGenerationPlan(
        name="test_column",
        faker_type="am_pm",
    )
    series = generate_series_from_plan(
        n=20,
        plan=plan,
    )

    assert series.notnull().all()
    assert series.shape == (20,)
    print(series[:5].tolist())
    assert ("AM" in series.tolist()) or ("PM" in series.tolist())
