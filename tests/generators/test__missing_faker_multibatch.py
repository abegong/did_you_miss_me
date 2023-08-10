"""Tests that verify that data generation methods work as expected."""

import pytest
import random


from did_you_miss_me.generators.multibatch import (
    MissingFakerMultiBatchGenerator
)
from did_you_miss_me.api import (
    generate_multibatch_dataframe,
)


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)


def test__create():
    generator = MissingFakerMultiBatchGenerator.create(
        exact_rows= 3,
        num_columns= 3,
        num_epochs= 3,
        batches_per_epoch= 3,
    )


def test__integer_primary_keys_are_continuous():
    generator = MissingFakerMultiBatchGenerator.create(
        exact_rows= 3,
        num_columns= 3,
        num_epochs= 3,
        batches_per_epoch= 3,
        include_primary_key=True,
    )
    df = generator.generate()
    print(df.columns)
    assert df.shape == (27, 4)
    print(list(df["column_primary_key"]))
    print([185128+x for x in range(27)])
    assert (df["column_primary_key"] == [str(634120+x) for x in range(27)]).all()
