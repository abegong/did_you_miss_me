"""Tests that verify that Plan objects work as expected: constructors, serialization, etc."""

import pytest
import random


from did_you_miss_me.generators.timestamps_and_ids import (
    TimestampAndIdWidget,
)


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)


def test__timestamp_and_id_column_generator():
    generator = TimestampAndIdWidget.create()
    generator.generate(
        num_rows=5,
    )
