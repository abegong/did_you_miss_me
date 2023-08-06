"""
Public-facing methods for generating synthetic missingness data.
"""

import pandas as pd
from typing import Optional

from did_you_miss_me.series_generators import (
    missify_series_from_plan,
)
from did_you_miss_me.plans import (
    ColumnMissingnessModifier,
    FakerColumnGenerator,
    MissingFakerColumnGenerator,
    MultiBatchGenerator,
)


def generate_series(
    n: int = 200,
) -> pd.Series:
    plan = FakerColumnGenerator(
        name="my_column",
    )
    series = plan.generate(
        n=n,
    )

    return series


def generate_dataframe(
    exact_rows: int = 200,
    num_columns: int = 12,
    add_missingness=True,
    # include_ids = False,
    # include_timestamps = False,
    # use_ai = False,
) -> pd.DataFrame:
    """Generate synthetic datasets with realistic patterns of missingness.

    Parameters:
    - num_rows (int): The number of rows to generate in the dataset.
    - num_columns (int): The number of columns to generate in the dataset.
    - add_missingness (bool): Whether to add missingness to the dataset.
    - include_ids (bool): Whether to include a columns simulating primary and foreign keys in the dataset.
    - include_timestamps (bool): Whether to include a timestamp column (or columns) in the dataset.
    - use_ai (bool): Whether to use artificial intelligence to generate the missingness patterns.
    """

    series_dict = {}
    for i in range(num_columns):
        column_generator = MissingFakerColumnGenerator.create(
            name=f"column_{i + 1}",
        )
        new_series = column_generator.generate(
            n=exact_rows,
        )

        if add_missingness:
            missified_series = missify_series_from_plan(
                new_series,
                plan=column_generator,
            )
        else:
            missified_series = new_series

        series_dict[column_generator.name] = missified_series

    df = pd.DataFrame(series_dict)

    return df


def missify_dataframe(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Add missingness to an existing dataframe."""
    series_dict = {}
    for i, column in enumerate(df.columns):
        column_modifier = ColumnMissingnessModifier.create()
        missified_series = missify_series_from_plan(
            df[column],
            plan=column_modifier,
        )
        series_dict[column] = missified_series

    df = pd.DataFrame(series_dict)
    return df


def generate_multibatch_dataframe(
    exact_rows: int = 200,
    num_columns: int = 12,
    num_epochs: int = 5,
    batches_per_epoch: Optional[int] = None,
    add_missingness=True,
    # include_ids = False,
    # include_timestamps = False,
    # use_ai = False,
) -> pd.DataFrame:
    """Generate synthetic datasets with realistic patterns of missingness.

    Parameters:
    - num_epochs (int): The number of epochs to generate in the dataset.
    - add_missingness (bool): Whether to add missingness to the dataset.
    """

    multibatch_plan = MultiBatchGenerator(
        exact_rows=exact_rows,
        num_columns=num_columns,
        num_epochs=num_epochs,
        batches_per_epoch=batches_per_epoch,
    )

    multibatch_df = pd.DataFrame()

    batch_id = 0
    for j, epoch_plan in enumerate(multibatch_plan.epochs):
        # print(f"Epoch: {j} of {multibatch_plan.num_epochs}")

        for k in range(epoch_plan.num_batches):
            # print(f"Batch: {k} of {epoch_plan.num_batches}")

            series_dict = {}
            batch_id_series = pd.Series([batch_id] * epoch_plan.dataframe_plan.num_rows)
            series_dict["batch_id"] = batch_id_series

            for i, column_generator in enumerate(
                epoch_plan.dataframe_plan.column_generators
            ):
                new_series = column_generator.generate(
                    n=epoch_plan.dataframe_plan.num_rows,
                )

                if add_missingness:
                    column_modifier = column_generator

                    missified_series = missify_series_from_plan(
                        new_series,
                        plan=column_modifier,
                    )

                else:
                    missified_series = new_series

                series_dict[column_generator.name] = missified_series

            df = pd.DataFrame(series_dict)
            multibatch_df = pd.concat([multibatch_df, df], ignore_index=True)

            batch_id += 1

    return multibatch_df
