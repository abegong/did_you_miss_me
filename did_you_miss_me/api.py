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

    return series


def generate_dataframe(
    exact_rows: int = 200,
    num_columns: int = 12,
    add_missingness=True,
    include_batch_id=False,
    include_primary_key=False,
    include_foreign_keys=False,
    include_timestamps=False,
    # use_ai = False,
) -> pd.DataFrame:
    """Generate synthetic datasets with realistic patterns of missingness.

    Parameters:
    - exact_rows (int): The number of rows to generate in the dataset.
    - num_columns (int): The number of columns to generate in the dataset.
    - add_missingness (bool): Whether to add missingness to the dataset.
    - include_batch_id (bool): Whether to include a column simulating a batch ID in the dataset.
    - include_primary_key (bool): Whether to include a column simulating a primary key in the dataset.
    - include_foreign_keys (bool): Whether to include columns simulating foreign keys in the dataset.
    - include_timestamps (bool): Whether to include a timestamp column (or columns) in the dataset.
    - use_ai (bool): Whether to use artificial intelligence to generate the missingness patterns.
    """

    dataframe_generator = MissingFakerDataframeGenerator.create(
        exact_rows=exact_rows,
        num_columns=num_columns,
        include_batch_id=include_batch_id,
        include_primary_key=include_primary_key,
        include_foreign_keys=include_foreign_keys,
        include_timestamps=include_timestamps,
        add_missingness=add_missingness,
    )
    result_object = dataframe_generator.generate()
    return result_object.dataframe


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
    exact_rows: Optional[int] = None,
    num_columns: int = 12,
    num_epochs: int = 5,
    batches_per_epoch: Optional[int] = None,
    add_missingness=True,
    include_batch_id=False,
    include_primary_key=False,
    include_foreign_keys=False,
    include_timestamps=True,
    # use_ai = False,
    print_updates=True,
) -> pd.DataFrame:
    """Generate synthetic datasets with realistic patterns of missingness.

    Parameters:
    - exact_rows (int): The number of rows to generate in the dataset.
    - num_columns (int): The number of columns to generate in the dataset.
    - num_epochs (int): The number of epochs to generate in the dataset.
    - batches_per_epoch (int): The number of batches to generate in each epoch.
    - add_missingness (bool): Whether to add missingness to the dataset.
    - include_batch_id (bool): Whether to include a column simulating a batch ID in the dataset.
    - include_primary_key (bool): Whether to include a column simulating a primary key in the dataset.
    - include_foreign_keys (bool): Whether to include columns simulating foreign keys in the dataset.
    - include_timestamps (bool): Whether to include a timestamp column (or columns) in the dataset.
    - use_ai (bool): Whether to use artificial intelligence to generate the missingness patterns.
    """

    multibatch_generator = MissingFakerMultiBatchGenerator.create(
        exact_rows=exact_rows,
        num_columns=num_columns,
        num_epochs=num_epochs,
        batches_per_epoch=batches_per_epoch,
        include_batch_id=include_batch_id,
        include_primary_key=include_primary_key,
        include_foreign_keys=include_foreign_keys,
        include_timestamps=include_timestamps,
        add_missingness=add_missingness,
    )

    df = multibatch_generator.generate(
        print_updates=print_updates,
    )
    return df

def _convert_df_to_sql_friendly(
    df : pd.DataFrame
) -> pd.DataFrame:
    type_conversion = {
        "object": object,
        "float64": float,
        "int64": int,
        'datetime64[ns]': int,
    }

    df_copy = df.copy()
    
    convert_dict = []
    for i, column in enumerate(df_copy.columns):
        converted_type = type_conversion[str(df_copy.dtypes[i])]
        convert_dict.append((column, converted_type))
    
    convert_dict = dict(convert_dict)

    df_copy = df_copy.astype(convert_dict)

    return df_copy
 
def generate_multiple_batches_and_upload_to_sql(
    conn,
    table_name,
    if_exists="replace",
    *args,
    **kwargs,
) -> None:
    df = generate_multibatch_dataframe(
        *args,
        **kwargs,
    )
    df = _convert_df_to_sql_friendly(df)
    df.to_sql(
        table_name,
        conn,
        if_exists=if_exists,
        index=None,
    )
