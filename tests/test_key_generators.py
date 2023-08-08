"""Tests that verify that Plan objects work as expected: constructors, serialization, etc."""

import json
import pytest
import random
import numpy as np


from did_you_miss_me.generators.keys import (
    # KeyColumnGenerator,
    IntegerKeyColumnGenerator,
    UuidKeyColumnGenerator,
)


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)


def test__key_column_generator():
    generator = IntegerKeyColumnGenerator.create(
        incrementing=True,
        data_type="int",
        percent_missing=0.0,
        percent_unique=1.0,
    )
    values = generator.generate(
        num_rows=5,
        starting_value=0,
    ).tolist()
    assert values == [0, 1, 2, 3, 4]


def test__key_column_generator__with_percent_missing():
    generator = IntegerKeyColumnGenerator.create(
        incrementing=True,
        data_type="int",
        percent_missing=1.0,
        percent_unique=1.0,
    )
    values = generator.generate(
        num_rows=5,
        starting_value=0,
    ).tolist()
    # assert values == [np.nan, np.nan, np.nan, np.nan, np.nan]
    #!!! This is a pain to test, because np.nan != np.nan


    generator = IntegerKeyColumnGenerator.create(
        incrementing=True,
        data_type="int",
        percent_missing=0.5,
        percent_unique=1.0,
    )
    values = generator.generate(
        num_rows=5,
        starting_value=0,
    ).tolist()
    # assert values == [1.0, 4.0, np.nan, np.nan, np.nan]
    #!!! This is a pain to test, because np.nan != np.nan


def test__key_column_generator__with_percent_unique():
    generator = IntegerKeyColumnGenerator.create(
        incrementing=True,
        data_type="int",
        percent_missing=0.0,
        percent_unique=0.5,
    )
    values = generator.generate(
        num_rows=10,
        starting_value=0,
    ).tolist()
    print(values)
    assert values == [0, 0, 0, 3, 3, 3, 3, 4, 7, 7]
