import random
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

import pandas as pd

from did_you_miss_me.generators.column import (
    ColumnGenerator,
    MultiColumnGenerator,
)
from did_you_miss_me.generators.keys import (
    IntegerKeyColumnGenerator,
)
from did_you_miss_me.generators.timestamp import (
    TimestampMultiColumnGenerator,
)


class Indexes(BaseModel):
    primary_key: Optional[int] = None
    timestamp: Optional[int] = None
    batch_id: Optional[int] = None

    @classmethod
    def create(
        cls,
        primary_key: Optional[int] = None,
        timestamp: Optional[int] = None,
        batch_id: Optional[int] = None,
    ) -> "Indexes":
        if primary_key is None:
            primary_key = random.randint(0, 1000000)

        if timestamp is None:
            timestamp = random.randint(0, 1000000)

        if batch_id is None:
            batch_id = random.randint(0, 1000000)

        return cls(
            primary_key=primary_key,
            timestamp=timestamp,
            batch_id=batch_id,
        )

class TimestampAndIdResultObject(BaseModel):

    columns: Dict[str, Any]#pd.Series]
    next_indexes: Indexes


class TimestampAndIdWidget(BaseModel):
    """Specifies how to create one or more columns containing timestamps and IDs."""

    primary_key_column_generator: Optional[IntegerKeyColumnGenerator] = Field(
        default_factory=IntegerKeyColumnGenerator.create_primary_key,
        description="The primary key column generator",
    )
    foreign_key_column_generators: List[ColumnGenerator] = Field(
        default_factory=lambda: [IntegerKeyColumnGenerator.create_foreign_key()],
        description="The column generators",
    )
    timestamp_column_generator: Optional[MultiColumnGenerator] = Field(
        default_factory=TimestampMultiColumnGenerator.create,
        description="The timestamp column generator",
    )

    @classmethod
    def create(
        cls,
        include_ids: bool = False,
        include_timestamps: bool = False,
    ) -> "TimestampAndIdWidget":
        names = []

        if include_ids:
            primary_key_column_generator = IntegerKeyColumnGenerator.create_primary_key()
            names = [primary_key_column_generator.name]

            foreign_key_column_generators = []
            if random.random() < 0.5:
                while 1:
                    new_key_generator = IntegerKeyColumnGenerator.create_foreign_key()
                    foreign_key_column_generators.append(new_key_generator)

                    names += [new_key_generator.name]

                    if random.random() < 0.7:
                        break

        else:
            primary_key_column_generator = None
            foreign_key_column_generators = []

        if include_timestamps:
            timestamp_column_generator = TimestampMultiColumnGenerator.create()
            names += timestamp_column_generator.names

        else:
            timestamp_column_generator = None

        return cls(
            names=names,
            primary_key_column_generator=primary_key_column_generator,
            foreign_key_column_generators=foreign_key_column_generators,
            timestamp_column_generator=timestamp_column_generator,
        )

    def generate(
        self,
        num_rows: int,
        next_indexes: Indexes,
    ) -> TimestampAndIdResultObject:
        """Generate series with the specified number of rows."""

        series_dict = {}

        if self.primary_key_column_generator is not None:
            new_series = self.primary_key_column_generator.generate(
                num_rows=num_rows,
                starting_value=next_indexes.primary_key,
            )

            series_dict[self.primary_key_column_generator.name] = new_series

        for i, column_generator in enumerate(self.foreign_key_column_generators):
            new_series = column_generator.generate(
                num_rows=num_rows,
            )

            series_dict[column_generator.name] = new_series

        if self.timestamp_column_generator is not None:
            timestamp_series_dict = self.timestamp_column_generator.generate(
                num_rows=num_rows,
            )

            series_dict = {**series_dict, **timestamp_series_dict}

        next_primary_key = next_indexes.primary_key + num_rows

        return TimestampAndIdResultObject(
            columns=series_dict,
            next_indexes=Indexes(
                primary_key=next_primary_key,
                timestamp=next_indexes.timestamp + num_rows, #!!! Not right
                batch_id=0,
            ),
        )
