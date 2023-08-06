"""
Public-facing methods for generating synthetic missingness data.
"""

import pandas as pd

from did_you_miss_me.plan_generators import (
    generate_column_plan,
    generate_column_missingness_plan,
)
from did_you_miss_me.series_generators import (
    generate_series_from_plan,
    missify_series_from_plan,
)
from did_you_miss_me.plans import (
    MultiBatchPlan,
)


def generate_series(
    n: int = 200,
) -> pd.Series:
    plan = generate_column_plan(column_index=1)
    series = generate_series_from_plan(
        n=n,
        plan=plan,
    )

    return series


def generate_dataframe(
    n_rows: int = 200,
    n_columns: int = 12,
    add_missingness = True,
    # include_ids = False,
    # include_timestamps = False,
    # use_ai = False,
) -> pd.DataFrame:
    """Generate synthetic datasets with realistic patterns of missingness.

    Parameters:
    - n_rows (int): The number of rows to generate in the dataset.
    - n_columns (int): The number of columns to generate in the dataset.
    - add_missingness (bool): Whether to add missingness to the dataset.
    - include_ids (bool): Whether to include a columns simulating primary and foreign keys in the dataset.
    - include_timestamps (bool): Whether to include a timestamp column (or columns) in the dataset.
    - use_ai (bool): Whether to use artificial intelligence to generate the missingness patterns.
    """

    series_dict = {}
    for i in range(n_columns):
        column_plan = generate_column_plan(column_index=i + 1)
        new_series = generate_series_from_plan(
            n=n_rows,
            plan=column_plan,
        )
        
        if add_missingness:
            missified_series = missify_series_from_plan(
                new_series,
                plan=column_plan,
            )
        else:
            missified_series = new_series

        series_dict[column_plan.name] = missified_series

    df = pd.DataFrame(series_dict)

    return df


def missify_dataframe(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Add missingness to an existing dataframe."""
    series_dict = {}
    for i, column in enumerate(df.columns):
        column_plan = generate_column_missingness_plan(
            column_index=i + 1,
        )
        missified_series = missify_series_from_plan(
            df[column],
            plan=column_plan,
        )
        series_dict[column] = missified_series

    df = pd.DataFrame(series_dict)
    return df


def generate_multibatch_dataframe(
    # n_rows: int = 200,
    # n_columns: int = 12,
    n_epochs: int = 5,
    add_missingness = True,
    # include_ids = False,
    # include_timestamps = False,
    # use_ai = False,
) -> pd.DataFrame:
    """Generate synthetic datasets with realistic patterns of missingness.

    Parameters:
    - n_rows (int): The number of rows to generate in the dataset.
    - n_columns (int): The number of columns to generate in the dataset.
    - add_missingness (bool): Whether to add missingness to the dataset.
    - include_ids (bool): Whether to include a columns simulating primary and foreign keys in the dataset.
    - include_timestamps (bool): Whether to include a timestamp column (or columns) in the dataset.
    - use_ai (bool): Whether to use artificial intelligence to generate the missingness patterns.
    """

    multibatch_plan = MultiBatchPlan()

    multibatch_df = pd.DataFrame()

    batch_id = 0
    for j, epoch_plan in enumerate(multibatch_plan.epochs):
        # print(f"Epoch: {j} of {multibatch_plan.num_epochs}")

        for k in range(epoch_plan.num_batches):    
            # print(f"Batch: {k} of {epoch_plan.num_batches}")

            series_dict = {}
            batch_id_series = pd.Series([batch_id] * epoch_plan.dataframe_plan.num_rows)
            series_dict["batch_id"] = batch_id_series

            for i, column_generation_plan in enumerate(epoch_plan.dataframe_plan.column_plans):

                new_series = generate_series_from_plan(
                    n=epoch_plan.dataframe_plan.num_rows,
                    plan=column_generation_plan,
                )
                
                if add_missingness:
                    column_plan = epoch_plan.dataframe_plan.column_plans[i]

                    missified_series = missify_series_from_plan(
                        new_series,
                        plan=column_plan,
                    )

                else:
                    missified_series = new_series

                series_dict[column_generation_plan.name] = missified_series

            df = pd.DataFrame(series_dict)
            multibatch_df = pd.concat([multibatch_df, df], ignore_index=True)

            batch_id += 1

    return multibatch_df