from abc import ABC
from enum import Enum
import random
from typing import Any, List, Optional

import pandas as pd

from did_you_miss_me.abc import (
    DataGenerator,
)
from did_you_miss_me.generators.column import (
    ColumnGenerator,
    MultiColumnGenerator,
)
from did_you_miss_me.generators.primary_key_generators import (
    PrimaryKeyColumnGenerator,
)
from did_you_miss_me.generators.timestamp import (
    TimestampColumnGenerator,
)
from did_you_miss_me.generators.foreign_keys import (
    ForeignKeyGenerator,
)

class TimeStampAndIdGenerator(MultiColumnGenerator):
    """Specifies how to create one or more columns containing timestamps and IDs."""

    id_column_generators: List[ColumnGenerator]
    timestamp_column_generator: Optional[MultiColumnGenerator]

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
        
        names = []

        if include_ids:
            id_column_generators = [PrimaryKeyColumnGenerator.create(
                name="column_primary_key",
            )]
            names = ["column_primary_key"]

            if random.random() < 0.5:
                id_column_generators.append(ForeignKeyGenerator.create(
                    name="column_foreign_key",
                ))

                names += ["column_foreign_key"]

        else:
            id_column_generators = []

        if include_timestamps:
            timestamp_column_generator = TimestampColumnGenerator.create()
            names += timestamp_column_generator.names
        
        else:
            timestamp_column_generator = None

        return cls(
            names=names,
            id_column_generators=id_column_generators,
            timestamp_column_generator=timestamp_column_generator,
        )