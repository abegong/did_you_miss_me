"""
Public-facing methods for generating synthetic missingness data.
"""

import pandas as pd
from typing import Optional

from did_you_miss_me.generators.column import (
    MissingFakerColumnGenerator,
)
from did_you_miss_me.generators.dataframe import (
    MissingFakerDataframeGenerator,
)
from did_you_miss_me.generators.multibatch import (
    MissingFakerMultiBatchGenerator,
)
from did_you_miss_me.modifiers.missingness import (
    ColumnMissingnessModifier,
)


def generate_series(
    num_rows: int = 200,
) -> pd.Series:
    """Generate a synthetic series with realistic patterns of missingness.
    
    Parameters:
    - num_rows (int): The number of rows to generate in the series.
    """

    generator = MissingFakerColumnGenerator.create(
        name="my_column",
        missingness_type="PROPORTIONAL",
    )
    series = generator.generate(
        num_rows=num_rows,
    )
    print(series)

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
    - exact_rows (int): The number of rows to generate in the dataset.
    - num_columns (int): The number of columns to generate in the dataset.
    - add_missingness (bool): Whether to add missingness to the dataset.
    - include_ids (bool): Whether to include a columns simulating primary and foreign keys in the dataset.
    - include_timestamps (bool): Whether to include a timestamp column (or columns) in the dataset.
    - use_ai (bool): Whether to use artificial intelligence to generate the missingness patterns.
    """

    dataframe_generator = MissingFakerDataframeGenerator.create(
        exact_rows=exact_rows,
        num_columns=num_columns,
    )
    df = dataframe_generator.generate(
        add_missingness=add_missingness,
    )
    return df


def missify_dataframe(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Add missingness to an existing dataframe.
    
    Parameters:
    - df (pd.DataFrame): The dataframe to add missingness to.
    """

    series_dict = {}
    for i, column in enumerate(df.columns):
        column_modifier = ColumnMissingnessModifier.create()
        missified_series = column_modifier.modify(
            df[column],
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
    # include_ids = True,
    # include_timestamps = True,
    # use_ai = False,
) -> pd.DataFrame:
    """Generate synthetic datasets with realistic patterns of missingness.

    Parameters:
    - exact_rows (int): The number of rows to generate in the dataset.
    - num_columns (int): The number of columns to generate in the dataset.
    - num_epochs (int): The number of epochs to generate in the dataset.
    - batches_per_epoch (int): The number of batches to generate in each epoch.
    - add_missingness (bool): Whether to add missingness to the dataset.
    - include_ids (bool): Whether to include a columns simulating primary and foreign keys in the dataset.
    - include_timestamps (bool): Whether to include a timestamp column (or columns) in the dataset.
    - use_ai (bool): Whether to use artificial intelligence to generate the missingness patterns.
    """

    multibatch_generator = MissingFakerMultiBatchGenerator.create(
        exact_rows=exact_rows,
        num_columns=num_columns,
        num_epochs=num_epochs,
        batches_per_epoch=batches_per_epoch,
    )

    df = multibatch_generator.generate()
    return df
