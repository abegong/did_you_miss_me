""" Tests for top-level API methods """

import pytest
import random

import pandas as pd

import did_you_miss_me as dymm


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)


def test__generate_series():
    random.seed(9)

    series = dymm.generate_series()
    assert series.shape == (200,)
    assert series.isnull().sum() > 0

    series = dymm.generate_series(
        num_rows=20,
    )
    assert series.shape == (20,)


def test__generate_dataframe():
    df = dymm.generate_dataframe(
        exact_rows=20,
        num_columns=10,
    )
    assert df.shape == (20, 10)
    assert df.isnull().sum().sum() > 0

    df = dymm.generate_dataframe(
        exact_rows=20,
        num_columns=10,
        add_missingness=False,
    )
    assert df.isnull().sum().sum() == 0

    df = dymm.generate_dataframe(
        exact_rows=20,
        num_columns=10,
        include_batch_id=True,
        include_primary_key=True,
        include_foreign_keys=True,
    )
    assert df.shape[1] > 10

    df = dymm.generate_dataframe(
        exact_rows=20,
        num_columns=10,
        include_timestamps=True,
    )
    assert df.shape[1] > 10


# Other parameters to test:
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


def test__generate_multibatch_dataframe():
    dymm.generate_multibatch_dataframe(
        num_columns=2,
        # num_rows=20,
        num_epochs=2,
        batches_per_epoch=2,
    )

    df = dymm.generate_multibatch_dataframe(
        num_columns=2,
        exact_rows=20,
        num_epochs=2,
        batches_per_epoch=2,
        include_batch_id=False,
        include_primary_key=False,
        include_foreign_keys=False,
        include_timestamps=False,
    )

    assert df.shape == (80, 2)
    assert df.isnull().sum().sum() > 0

    df = dymm.generate_multibatch_dataframe(
        num_columns=2,
        exact_rows=20,
        num_epochs=2,
        batches_per_epoch=2,
        add_missingness=False,
        include_batch_id=False,
        include_primary_key=False,
        include_foreign_keys=False,
        include_timestamps=False,
    )
    assert df.shape == (80, 2)
    assert df.isnull().sum().sum() == 0

    df = dymm.generate_multibatch_dataframe(
        num_columns=2,
        exact_rows=20,
        num_epochs=2,
        batches_per_epoch=2,
        include_batch_id=True,
        include_primary_key=True,
        include_foreign_keys=True,
        include_timestamps=False,
    )
    assert df.shape[1] > 2

    df = dymm.generate_multibatch_dataframe(
        num_columns=2,
        exact_rows=20,
        num_epochs=2,
        batches_per_epoch=2,
        include_batch_id=False,
        include_primary_key=False,
        include_foreign_keys=False,
        include_timestamps=True,
    )
    assert df.shape[1] > 2

    df = dymm.generate_multibatch_dataframe(
        num_columns=2,
        exact_rows=20,
        num_epochs=2,
        batches_per_epoch=2,
    )
    assert df.shape[1] > 2

    # print(df.column_primary_key)
    # assert (df["column_primary_key"] == range(80)).all()

def test__generate_multiple_batches_and_upload_to_sql():
    random.seed(0)

    import sqlite3
    conn = sqlite3.connect(":memory:")

    dymm.generate_multiple_batches_and_upload_to_sql(
        conn=conn,
        table_name="test_table",
        num_epochs=2,
        exact_rows=5,
        batches_per_epoch=10,
    )