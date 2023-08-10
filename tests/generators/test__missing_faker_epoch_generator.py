"""Tests that verify that data generation methods work as expected."""

import json
import pytest
import random


from did_you_miss_me.generators.multibatch import (
    MissingFakerEpochGenerator
)

@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)


def test__MissingFakerEpochGenerator__create():
    # This is just a smoke test to make sure that the generator can be constructed.
    generator = MissingFakerEpochGenerator.create(
        num_batches=3,
        # min_rows=10,
        # max_rows=20,
    )
    print(json.dumps(generator.model_dump(), indent=2))
    # generator.generate()
    