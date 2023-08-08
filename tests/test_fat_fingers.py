"""Tests that verify that missifying methods work as expected."""

import pytest
import random

import pandas as pd

from did_you_miss_me.generators.column import (
    FakerColumnGenerator,
)
from did_you_miss_me.modifiers.fat_fingers import (
    ColumnFatFingersModifier,
)

# @pytest.fixture(autouse=True)
# def set_random_seed():
#     random.seed(1)

# @pytest.fixture()
# def faked_full_names():
#     series = FakerColumnGenerator.create(
#         faker_type="full_name",
#     ).generate(
#         num_rows=20,
#     )

def test___modify_values():
    """Tests that the __modify_values method works as expected."""

    test_string = "abcd"

    # Print out some examples, for manual inspection.
    error_types = [
        "missing_chars",
        "extra_chars",
        "transposed_chars",
        "mistaken_chars",
        "repeated_chars",
    ]

    for error_type in error_types:
        print(f"##### {error_type} #####")
        for i in range(10):
            print(ColumnFatFingersModifier._modify_value(test_string, error_type))

    random.seed(1)
    assert ColumnFatFingersModifier._modify_value(test_string, "missing_chars") == "acd"
    assert ColumnFatFingersModifier._modify_value(test_string, "extra_chars") == "cabcd"
    assert ColumnFatFingersModifier._modify_value(test_string, "transposed_chars") == "bacd"
    assert ColumnFatFingersModifier._modify_value(test_string, "mistaken_chars") == "abc3"
    assert ColumnFatFingersModifier._modify_value(test_string, "repeated_chars") == "abcdd"


def test___modify_column():
    modifier = ColumnFatFingersModifier.create(
        error_rate=0.5,
    )
    
    full_names = FakerColumnGenerator(
        faker_type="name",
    ).generate(
        num_rows=20,
    )
    print(type(full_names))

    modified_full_names = modifier.modify(full_names)
    print(full_names)
    print(modified_full_names)

    numbers = pd.Series([str(random.randint(10000, 99999)) for _ in range(20)])

    modified_numbers = modifier.modify(numbers)
    print(numbers)
    print(modified_numbers)