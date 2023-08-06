"""Tests that verify that missifying methods work as expected."""

import pytest
import random

import pandas as pd

from did_you_miss_me.modifiers.missingness import (
    ColumnMissingnessType,
    ColumnMissingnessModifier,
    ProportionalColumnMissingnessParams,
)


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(1)


#!!! Rename
def test__missify_series_from_plan():
    series = pd.Series(range(100))

    # Test with missingness_type=ALWAYS
    column_modifier = ColumnMissingnessModifier.create(
        missingness_type=ColumnMissingnessType.ALWAYS,
    )
    new_series = column_modifier.modify(
        series=series,
    )
    assert new_series.isna().all()
    assert new_series.shape == series.shape

    # Test with missingness_type=NEVER
    column_modifier = ColumnMissingnessModifier.create(
        missingness_type=ColumnMissingnessType.NEVER,
    )
    new_series = column_modifier.modify(
        series=series,
    )
    assert not new_series.isna().any()
    assert new_series.shape == series.shape

    # Test with missingness_type=PROPORTIONAL
    column_modifier = ColumnMissingnessModifier.create(
        missingness_type=ColumnMissingnessType.PROPORTIONAL,
        missingness_params=ProportionalColumnMissingnessParams(
            proportion=0.5,
        ),
    )
    new_series = column_modifier.modify(
        series=series,
    )
    assert new_series.isna().sum() == 47  # About 50, but not exactly 50
    assert new_series.shape == series.shape

    # Any values that are not null are the same as the original series
    assert (new_series[new_series.notnull()] == series[new_series.notnull()]).all()
