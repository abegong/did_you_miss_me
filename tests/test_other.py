""" Miscellaneous tests for the missingness_data_generator package """

import pytest
import random

import pandas as pd

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


def test__missify_dataframe():
    df = pd.DataFrame(
        {
            "x": range(200),
            "y": range(200),
            "z": [str(i) for i in range(200)],
        }
    )
    missing_df = mdg.missify_dataframe(df)
    assert missing_df.shape == (200, 3)
    assert (df.x[missing_df.x.notnull()] == missing_df.x[missing_df.x.notnull()]).all()


def test__generate_series():
    random.seed(9)

    series = mdg.generate_series()
    print(series)
    assert series.shape == (200,)

    series = mdg.generate_series(
        n=1492,
    )
    print(series)
    assert series.shape == (1492,)

