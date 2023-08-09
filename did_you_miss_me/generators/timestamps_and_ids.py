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


class TimestampAndIdResultObject(BaseModel):

    last_primary_key: int
    last_timestamp: int

    columns: Dict[str, Any]#pd.Series]


class TimestampAndIdWidget(BaseModel):
    """Specifies how to create one or more columns containing timestamps and IDs."""

    names: List[str] = Field(
        default_factory=lambda: [f"column_{random.randint(0, 1000000)}"],
        description="The names of the columns",
    )
    id_column_generators: List[ColumnGenerator]
    timestamp_column_generator: Optional[MultiColumnGenerator]

    @classmethod
    def create(
        cls,
        include_ids: bool = False,
        include_timestamps: bool = False,
    ) -> "TimestampAndIdWidget":
        names = []

        if include_ids:
            id_column_generators = [IntegerKeyColumnGenerator.create_primary_key()]
            names = [id_column_generators[0].name]

            if random.random() < 0.5:
                while 1:
                    new_key_generator = IntegerKeyColumnGenerator.create_foreign_key()
                    id_column_generators.append(new_key_generator)

                    names += [new_key_generator.name]

                    if random.random() < 0.7:
                        break

        else:
            id_column_generators = []

        if include_timestamps:
            timestamp_column_generator = TimestampMultiColumnGenerator.create()
            names += timestamp_column_generator.names

        else:
            timestamp_column_generator = None

        return cls(
            names=names,
            id_column_generators=id_column_generators,
            timestamp_column_generator=timestamp_column_generator,
        )

    def generate(
        self,
        num_rows: int,
        starting_primary_key: int = 0,
        starting_timestamp: pd.Timestamp = pd.Timestamp("2020-01-01"),
    ) -> TimestampAndIdResultObject:
        """Generate series with the specified number of rows."""

        series_dict = {}

        for i, column_generator in enumerate(self.id_column_generators):
            new_series = column_generator.generate(
                num_rows=num_rows,
            )

            series_dict[column_generator.name] = new_series

        if self.timestamp_column_generator is not None:
            timestamp_series_dict = self.timestamp_column_generator.generate(
                num_rows=num_rows,
            )

            series_dict = {**series_dict, **timestamp_series_dict}

        return TimestampAndIdResultObject(
            columns=series_dict,
            last_primary_key=starting_primary_key + num_rows - 1,
            last_timestamp=0,#starting_timestamp + pd.Timedelta(days=num_rows - 1),
        )
