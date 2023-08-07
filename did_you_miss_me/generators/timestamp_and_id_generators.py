from abc import ABC
from enum import Enum
import random
from typing import Any, List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4

import pandas as pd

from did_you_miss_me.abc import (
    DataGenerator,
)
from did_you_miss_me.generators.column import (
    ColumnGenerator,
)
from did_you_miss_me.generators.primary_key_generators import (
    PrimaryKeyType,
    PrimaryKeyParams,
    PrimaryKeyColumnGenerator,
    IntegerPrimaryKeyParams,
)

### Foreign Keys ###

class ForeignKeyGenerator(ColumnGenerator):

    @classmethod
    def create(
        cls,
        name: Optional[str] = None,
    ) -> Any:
        """Create a ForeignKeyGenerator."""

        return cls(
            name=name,
        )

    def generate(self, num_rows:int ) -> pd.Series:
        return pd.Series(range(num_rows))

### Timestamps ###

class TimestampFormat(str, Enum):
    """Types of timestamp formats"""

    unix_epoch = "UNIX_EPOCH"
    iso_8601 = "ISO_8601"
    single_column_timestamp = "SINGLE_COLUMN_TIMESTAMP"
    multi_column_timestamp = "MULTI_COLUMN_TIMESTAMP"
    single_column_date = "SINGLE_COLUMN_DATE"
    multi_column_date = "MULTI_COLUMN_DATE"

class TimestampColumnGenerator(ColumnGenerator):

    timestamp_format: TimestampFormat

    @classmethod
    def create(
        cls,
        name: Optional[str] = None,
        timestamp_format: Optional[TimestampFormat] = None,
    ) -> Any:
        """Create a TimestampColumnGenerator."""

        if timestamp_format is None:
            timestamp_format = random.choice(list(TimestampFormat))

        return cls(
            name=name,
            timestamp_format=timestamp_format,
        )

    def generate(self, num_rows:int) -> pd.Series:
        return pd.Series(range(num_rows))

class MultiColumnGenerator(DataGenerator, ABC):
    """Abstract base class for generators that create multiple columns."""
    pass

### Timestamps and IDs ###

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
    ) -> "TimeStampAndIdGenerator":

        if include_ids:
            id_column_generators = [PrimaryKeyColumnGenerator.create(
                name="column_primary_key",
            )]

            if random.random() < 0.5:
                id_column_generators.append(ForeignKeyGenerator.create(
                    name="column_foreign_key",
                ))

        else:
            id_column_generators = []

        if include_timestamps:
            timestamp_column_generators = [TimestampColumnGenerator.create(
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