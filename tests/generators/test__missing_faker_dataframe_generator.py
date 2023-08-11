import pytest
import random

from did_you_miss_me.generators.dataframe import (
    MissingFakerDataframeGenerator
)

@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)


def test_create_instance():
    """
    Test if an instance of MissingFakerDataframeGenerator can be created.
    """
    generator = MissingFakerDataframeGenerator.create()
    assert isinstance(generator, MissingFakerDataframeGenerator), "Failed to create an instance."


def test_batch_id_not_included_by_default():
    """
    Test that 'column_batch_id' is not included in the dataframe columns by default.
    """
    result_object = MissingFakerDataframeGenerator.create().generate()
    df = result_object.dataframe
    assert "column_batch_id" not in df.columns, "'column_batch_id' should not be included by default."


def test_batch_id_included_when_flag_true():
    """
    Test that 'column_batch_id' is included in the dataframe columns when the flag is set to True.
    """
    result_object = MissingFakerDataframeGenerator.create(
        include_batch_id=True,
    ).generate()
    df = result_object.dataframe
    assert "column_batch_id" in df.columns, "'column_batch_id' should be included when flag is set to True."
