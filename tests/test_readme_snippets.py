"""Test the code snippets in the README.md file."""

import random

import pandas as pd

import did_you_miss_me as dymm


def test__generate_dataframe():
    random.seed(14)

    # Test that we can control the shape of the dataframe
    df = dymm.generate_dataframe(
        exact_rows=10,
        num_columns=8,
    )
    print(df)
    print(df.to_markdown())

    assert df.shape == (10, 8)


def test__missify_dataframe():
    random.seed(10)

    df = pd.read_csv(
        "https://projects.fivethirtyeight.com/polls/data/favorability_polls.csv"
    )
    assert df.shape == (2375, 38)

    columns = df.columns
    print(df[columns[:8]].head(10).to_markdown())

    missing_df = dymm.missify_dataframe(df)
    print(missing_df)
    print(missing_df.head())
    print(missing_df[columns[:8]].head(10).to_markdown())

    assert missing_df.shape == (2375, 38)
