"""Test the code snippets in the README.md file."""

import pandas as pd

import missingness_data_generator as mdg

# @pytest.fixture(autouse=True)
# def set_random_seed():
#     random.seed(42)


def test__generate_series():
    series = mdg.generate_series()
    print(series)
    assert series.shape == (200,)

    series = mdg.generate_series(
        n=1492,
    )
    print(series)
    assert series.shape == (1492,)


def test__generate_dataframe():
    df = mdg.generate_dataframe()
    print(df)

    # Test that we can control the shape of the dataframe
    df = mdg.generate_dataframe(
        n_rows=1492,
        n_columns=17,
    )
    assert df.shape == (1492, 17)
    print(df)


def test__missify_dataframe():
    df = pd.DataFrame(
        {
            "x": range(200),
            "y": range(200),
            "z": [str(i) for i in range(200)],
        }
    )

    missing_df = mdg.missify_dataframe(df)
    print(missing_df)

    assert missing_df.shape == (200, 3)
    assert (df.x[missing_df.x.notnull()] == missing_df.x[missing_df.x.notnull()]).all()
