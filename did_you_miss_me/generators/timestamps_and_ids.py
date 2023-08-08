from abc import ABC
from enum import Enum
import random
from typing import Any, Dict, List, Optional

import pandas as pd

from did_you_miss_me.abc import (
    DataGenerator,
)
from did_you_miss_me.generators.column import (
    ColumnGenerator,
    MultiColumnGenerator,
)
from did_you_miss_me.generators.keys import (
    KeyColumnGenerator,
    IntegerKeyColumnGenerator,
    UuidKeyColumnGenerator,
)
from did_you_miss_me.generators.timestamp import (
    TimestampMultiColumnGenerator,
)

class TimeStampAndIdMultiColumnGenerator(MultiColumnGenerator):
    """Specifies how to create one or more columns containing timestamps and IDs."""

    id_column_generators: List[ColumnGenerator]
    timestamp_column_generator: Optional[MultiColumnGenerator]

    @classmethod
    def create(
        cls,
        include_ids: bool = False,
        include_timestamps: bool = False,
    ) -> "TimeStampAndIdGenerator":
        
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
        num_rows: int
    ) -> Dict[str, pd.Series]:
        """Generate series with the specified number of rows."""

        series_dict = {}

        for i, column_generator in enumerate(self.id_column_generators):
            new_series = column_generator.generate(
                num_rows=num_rows,
                # add_missingness=add_missingness,
            )

            series_dict[column_generator.name] = new_series

        if self.timestamp_column_generator is not None:
            timestamp_series_dict = self.timestamp_column_generator.generate(
                num_rows=num_rows,
            )

            series_dict = {**series_dict, **timestamp_series_dict}
        
        return series_dict
