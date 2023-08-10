import pytest
import random

from did_you_miss_me.generators.dataframe import (
    MissingFakerDataframeGenerator
)

@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)


def test__create():
    generator = MissingFakerDataframeGenerator.create()

def test__create__batch_id():
    """batch_id is not included by default."""
    result_object = MissingFakerDataframeGenerator.create().generate()
    df = result_object.dataframe
    assert "column_batch_id" not in df.columns

    """batch_id is not included when batch_id=True."""
    result_object = MissingFakerDataframeGenerator.create(
        include_batch_id=True,
    ).generate()
    df = result_object.dataframe
    assert "column_batch_id" in df.columns
