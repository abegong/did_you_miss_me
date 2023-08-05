"""
Public-facing methods for generating missingness data.
"""

import pandas as pd

from missingness_data_generator.plan_generators import generate_column_plan
from missingness_data_generator.series_generators import (
    generate_series_from_plan,
    missify_series_from_plan,
)
from missingness_data_generator.generate_missing_data import generate_dataframe_with_missingness

def generate_series(
    n: int = 200,
) -> pd.Series:
    
    plan = generate_column_plan(
        column_index=1
    )
    series = generate_series_from_plan(
        n=n,
        plan=plan,
    )

    return series


def generate_dataframe(
    n_rows: int = 200,
    n_columns: int = 12,
    # include_ids = False,
    # include_timestamps = False,
    # use_ai = False,
) -> pd.DataFrame:
    """
    Generate synthetic datasets with realistic patterns of missingness.

    Parameters:
    - n_rows (int): The number of rows to generate in the dataset.
    - n_columns (int): The number of columns to generate in the dataset.
    - include_ids (bool): Whether to include a columns simluating primary and foreign keys in the dataset.
    - include_timestamps (bool): Whether to include a timestamp column (or columns) in the dataset.
    - use_ai (bool): Whether to use artificial intelligence to generate the missingness patterns.
    """
    
    
    df = generate_dataframe_with_missingness(
        n_rows=n_rows,
        n_columns=n_columns,
    )
    
    return df


def missify_dataframe(
    df: pd.DataFrame,
) -> pd.DataFrame:
    
    columns = df.columns
    n_rows = df.shape[0]
    n_columns = df.shape[1]

    series = {}
    for i, column in enumerate(df.columns):
        column_plan = generate_column_plan(
            column_index=i+1,
        )
        new_series = missify_series_from_plan(
            df[column],
            plan=column_plan,
        )
        series[column_plan.name] = new_series

    df = pd.DataFrame(series)
    return df