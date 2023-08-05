from typing import Optional, List

import pandas as pd

# from plans import (
#     ColumnPlan,
#     ProportinallyMissingColumnPlan,
#     ConditionallyMissingColumnPlan,
#     DataframePlan,
#     EpochPlan,
#     MultibatchPlan
# )

from missingness_data_generator.plan_generators import generate_column_plan
from missingness_data_generator.series_generators import generate_series_from_plan


def generate_dataframe_with_missingness(
    n_rows: int = 200, n_columns: int = 10, missingness_type_list: Optional[List] = None
) -> pd.DataFrame:
    """
    Generate synthetic datasets with realistic patterns of missingness.

    Parameters:
    - n_rows (int): The number of rows to generate in the dataset.
    - n_cols (int): The number of columns to generate in the dataset.
    - missingness_type_list (Optional[Dict[str, missingness_pattern]]): A dictionary of column names and patterns of
      missingness to use for populating the dataset. If omitted, columns and missingness categories will be created at
      random.
    """

    series = {}
    for i in range(n_columns):
        column_plan = generate_column_plan(column_index=i + 1)
        new_series = generate_series_from_plan(
            n=n_rows,
            plan=column_plan,
        )
        series[column_plan.name] = new_series

    df = pd.DataFrame(series)

    # series = []
    # for i in range(n_cols):
    #     type_, kwargs = generate_random_missingness_type_and_kwargs()
    #     new_series = generate_series_from_missingness_type_and_kwargs(
    #         n=n_rows,
    #         missingness_type=type_,
    #         missingness_kwargs=kwargs,
    #     )
    #     series.append(new_series)

    # columns = dict([
    #     (
    #         f"column_{i}",
    #         series[i],
    #     ) for i in range(n_cols)
    # ])

    # df = pd.DataFrame(columns)
    return df
