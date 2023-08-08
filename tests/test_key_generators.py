"""Tests that verify that Plan objects work as expected: constructors, serialization, etc."""

import json
import pytest
import random


from did_you_miss_me.generators.keys import (
    # KeyColumnGenerator,
    IntegerKeyColumnGenerator,
    UuidKeyColumnGenerator,
)


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)


def test__primary_key_column_generator():
    generator = IntegerKeyColumnGenerator.create(
        incrementing=True,
        data_type="int",
    )
    values = generator.generate(
        num_rows=5,
        starting_value=0,
    ).tolist()
    assert values == [0, 1, 2, 3, 4]


    # generator = IntegerKeyColumnGenerator.create(
    #     ascending=False,
    #     digits=10,
    # )
    # random.seed(40)
    # values = generator.generate(
    #     num_rows=5,
    # ).tolist()
    # print(values)
    # assert values == [136779594, 9802945638, 2853227234, 5791287653, 8712908219]

    # generator = IntegerKeyColumnGenerator.create(
    #     incrementing=False,
    #     ascending=False,
    #     digits=4,
    #     data_type="int",
    # )
    # random.seed(40)
    # values = generator.generate(
    #     num_rows=5,
    # ).tolist()
    # print(values)
    # assert values == [7513, 9494, 8584, 521, 4018]
    
    # generator = UuidKeyColumnGenerator.create()
    # values = generator.generate(
    #     num_rows=5,
    # ).tolist()
    # print(values)
    # #!!! Can't easily test this because it's random, and uuid uses a different random seed than random.seed()
    # # assert values == ['f3db7405-2813-4856-8e6e-19a002451365', 'fd56f8a9-36bb-4f03-8059-7f1ce7335c19', '939b751d-fadf-45d3-a73a-65457135076e', '926a5be1-3801-41c1-944f-203772f9b52f', 'eff9baf3-291d-4f64-ad6c-250ecbc46e9a']


    # # Composite key

