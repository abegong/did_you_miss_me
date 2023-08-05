"""
Public-facing methods for generating missingness data.
"""

import pandas as pd

from missingness_data_generator.plan_generators import generate_column_plan
from missingness_data_generator.series_generators import generate_series_from_plan
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
) -> pd.DataFrame:
    
    df = generate_dataframe_with_missingness(
        n_rows=n_rows,
        n_columns=n_columns,
    )
    
    return df


def missify_dataframe(
    df: pd.DataFrame,
) -> pd.DataFrame:
    raise NotImplementedError