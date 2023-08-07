from abc import ABC
import random
from typing import Any, List, Optional

import pandas as pd

from did_you_miss_me.abc import (
    DataGenerator,
)
from did_you_miss_me.generators.column import (
    ColumnGenerator,
)

class PrimaryKeyColumnGenerator(ColumnGenerator):
    """Specifies how to create a column containing a primary key."""

    # unique: bool = True
    # strictly_ascending: bool = True
    
    def generate(self, num_rows:int ) -> pd.Series:
        return pd.Series(range(num_rows))

class ForeignKeyGenerator(ColumnGenerator):

    # unique: bool = True
    # strictly_ascending: bool = True

    def generate(self, num_rows:int ) -> pd.Series:
        return pd.Series(range(num_rows))

class TimestampColumnGenerator(ColumnGenerator):

    # unique: bool = True
    # strictly_ascending: bool = True

    def generate(self, num_rows:int ) -> pd.Series:
        return pd.Series(range(num_rows))

class MultiColumnGenerator(DataGenerator, ABC):
    """Abstract base class for generators that create multiple columns."""
    pass


class TimeStampAndIdGenerator(MultiColumnGenerator):
    """Specifies how to create one or more columns containing timestamps and IDs."""

    id_column_generators: List[ColumnGenerator]
    timestamp_column_generators: List[ColumnGenerator]

    # has_primary_key: bool
    # foreign_key_column_names: List[str]

    # timestamp_column_names: List[str]
    # timestamp_column_formats: List[str]

    # timestamp_column_name: Optional[str]
    # exact_rows: Optional[int]
    # min_rows: Optional[int]
    # max_rows: Optional[int]

    @classmethod
    def create(
        cls,
        include_ids: bool = False,
        include_timestamps: bool = False,
    ) -> "TimeStampAndIdWidget":
        """Create a new instance of this class."""

        if include_ids:
            id_column_generators = [PrimaryKeyColumnGenerator(
                name="column_primary_key",
            )]

            if random.random() < 0.5:
                id_column_generators.append(ForeignKeyGenerator(
                    name="column_foreign_key",
                ))

        else:
            id_column_generators = []

        if include_timestamps:
            timestamp_column_generators = [TimestampColumnGenerator(
                name="column_timestamp",
            )]
        
        else:
            timestamp_column_generators = []

        return cls(
            id_column_generators=id_column_generators,
            timestamp_column_generators=timestamp_column_generators,
        )
    

    
# Possibilities:
#     single_primary_key
#     joint_primary_key
#     single_batch_id
#     joint_batch_id
#     single_timestamp
#     multicolumn_timestamp