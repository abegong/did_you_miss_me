""" Test all of the parameters of the generate_dataframe function. """

import pytest
import random

import missingness_data_generator as mdg

@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)

def test__generate_dataframe__with_add_missingness_equals_false():
    df = mdg.generate_dataframe(
        add_missingness=False,
    )
    assert df.isnull().sum().sum() == 0

    # - include_ids (bool): Whether to include a columns simulating primary and foreign keys in the dataset.
    # - include_timestamps (bool): Whether to include a timestamp column (or columns) in the dataset.
    # - use_ai (bool): Whether to use artificial intelligence to generate the missingness patterns.
