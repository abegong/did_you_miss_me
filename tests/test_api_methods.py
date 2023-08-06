""" Tests for top-level API methods """

import pytest
import random

import pandas as pd

import did_you_miss_me as dymm

@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)

def test__generate_dataframe__with_add_missingness_equals_false():
    df = dymm.generate_dataframe(
        num_rows=20,
        num_columns=10,
        add_missingness=False,
    )
    assert df.isnull().sum().sum() == 0

# Other parameters to test:
# - include_ids (bool): Whether to include a columns simulating primary and foreign keys in the dataset.
# - include_timestamps (bool): Whether to include a timestamp column (or columns) in the dataset.
# - use_ai (bool): Whether to use artificial intelligence to generate the missingness patterns.

def test__missify_dataframe():
    df = pd.DataFrame(
        {
            "x": range(100),
            "y": range(100),
            "z": [str(i) for i in range(100)],
        }
    )
    missing_df = dymm.missify_dataframe(df)
    assert missing_df.shape == (100, 3)
    assert (df.x[missing_df.x.notnull()] == missing_df.x[missing_df.x.notnull()]).all()


def test__generate_series():
    random.seed(9)

    series = dymm.generate_series()
    assert series.shape == (200,)

    series = dymm.generate_series(
        n=20,
    )
    assert series.shape == (20,)


def test__generate_multibatch_dataframe():
    df = dymm.generate_multibatch_dataframe(
        num_columns=2,
        num_rows=20,
        num_epochs=2,
        batches_per_epoch=2,
    )

    assert df.shape == (80, 3)