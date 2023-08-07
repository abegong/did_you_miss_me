"""Tests that verify that Plan objects work as expected: constructors, serialization, etc."""

import json
import pytest
import random


from did_you_miss_me.generators.timestamp import (
    TimestampMultiColumnGenerator,
    TimestampFormat,
)


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)


def test__timestamp_multi_column_generator():
    generator = TimestampMultiColumnGenerator.create()
    values = generator.generate(
        num_rows=5,
    )
    print(values)
