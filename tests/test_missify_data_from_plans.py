import pytest
import random

import pandas as pd

from missingness_data_generator.plans import (
    ColumnMissingnessType,
    ColumnMissingnessPlan,
    ProportionalColumnMissingnessPlan,
)
from missingness_data_generator.series_generators import (
    missify_series_from_plan,
)


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(1)


def test__missify_series_from_plan():
    series = pd.Series(range(100))

    # Test with missingness_type=ALWAYS
    plan = ColumnMissingnessPlan(
        missingness_type=ColumnMissingnessType.ALWAYS,
    )
    new_series = missify_series_from_plan(
        series=series,
        plan=plan,
    )
    assert new_series.isna().all()
    assert new_series.shape == series.shape

    # Test with missingness_type=NEVER
    plan = ColumnMissingnessPlan(
        missingness_type=ColumnMissingnessType.NEVER,
    )
    new_series = missify_series_from_plan(
        series=series,
        plan=plan,
    )
    assert not new_series.isna().any()
    assert new_series.shape == series.shape

    # Test with missingness_type=PROPORTIONAL
    plan = ProportionalColumnMissingnessPlan(
        missingness_type=ColumnMissingnessType.PROPORTIONAL,
        proportion=0.5,
    )
    new_series = missify_series_from_plan(
        series=series,
        plan=plan,
    )
    assert new_series.isna().sum() == 47  # About 50, but not exactly 50
    assert new_series.shape == series.shape

    # Any values that are not null are the same as the original series
    assert (new_series[new_series.notnull()] == series[new_series.notnull()]).all()
