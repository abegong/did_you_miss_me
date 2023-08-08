from abc import ABC
import datetime
from enum import Enum
import random
from typing import Any, List, Optional
from pydantic import BaseModel, Field

import pandas as pd

from did_you_miss_me.generators.column import (
    ColumnGenerator,
    MultiColumnGenerator,
)

### Timestamps ###

class TimestampFormat(str, Enum):
    """Types of timestamp formats"""

    UNIX_EPOCH = "UNIX_EPOCH"
    ISO_8601 = "ISO_8601"
    SINGLE_COLUMN_TIMESTAMP = "SINGLE_COLUMN_TIMESTAMP"
    MULTI_COLUMN_TIMESTAMP = "MULTI_COLUMN_TIMESTAMP"
    SINGLE_COLUMN_DATE = "SINGLE_COLUMN_DATE"
    MULTI_COLUMN_DATE = "MULTI_COLUMN_DATE"

class TimestampMultiColumnGenerator(MultiColumnGenerator):

    timestamp_format: TimestampFormat
    start_time: Optional[int] = Field(
        None,
        description="The start time for the timestamp column in seconds since the Unix epoch.",
    )
    end_time: Optional[int] = Field(
        None,
        description="The end time for the timestamp column in seconds since the Unix epoch.",
    )
    sortedness: float = Field(
        1.0,
        description="A number between 0 and 1 indicating how sorted the timestamp column should be. 0 means completely unsorted, 1 means completely sorted.",
    )

    @classmethod
    def create(
        cls,
        names: Optional[str] = None,
        timestamp_format: Optional[TimestampFormat] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        sortedness: Optional[float] = None,
    ) -> Any:
        """Create a TimestampColumnGenerator."""

        if timestamp_format is None:
            timestamp_format = random.choice(list(TimestampFormat))

        if end_time is None:
            # Get the current unix epoch
            end_time = int(datetime.datetime.now().timestamp())

        if start_time is None:
            start_time = end_time - 3600*24*random.randint(1, 365)

        assert start_time <= end_time, "start_time must be less than or equal to end_time"

        if sortedness is None:
            sortedness = 1 - (random.random()**2)

        if names is None:
            names = cls.get_column_names(timestamp_format)

        return cls(
            names=names,
            timestamp_format=timestamp_format,
            start_time=start_time,
            end_time=end_time,
            sortedness=sortedness,
        )

    def generate(
        self,
        num_rows:int,
        seed: Optional[int] = None,
    ) -> List[pd.Series]:
        """Generate a timestamp column."""
    
        if seed is not None:
            random.seed(seed)

        # Create a series of random timestamps
        series = pd.Series([random.randint(self.start_time, self.end_time) for _ in range(num_rows)])

        # Sort the series, at least partially
        sortedish_series = self.partial_sort(series, self.sortedness)

        # Format the series, depending on the timestamp format
        formatted_series = self._reformat_series(sortedish_series)

        return dict(zip(self.names, formatted_series))
    
    def _reformat_series(self, series: pd.Series) -> pd.Series:
        """Reformat a series of timestamps."""

        if self.timestamp_format == TimestampFormat.UNIX_EPOCH:
            formatted_series = [series]
        
        elif self.timestamp_format == TimestampFormat.ISO_8601:
            formatted_series = [series.apply(datetime.datetime.fromtimestamp)]
        
        elif self.timestamp_format == TimestampFormat.SINGLE_COLUMN_TIMESTAMP:
            formatted_series = [series.apply(datetime.datetime.fromtimestamp).apply(str)]
        
        elif self.timestamp_format == TimestampFormat.MULTI_COLUMN_TIMESTAMP:
            date_series = series.apply(datetime.datetime.fromtimestamp).apply(lambda x: x.date())
            time_series = series.apply(datetime.datetime.fromtimestamp).apply(lambda x: x.time())

            formatted_series = [date_series, time_series]
        
        elif self.timestamp_format == TimestampFormat.SINGLE_COLUMN_DATE:
            formatted_series = [series.apply(datetime.datetime.fromtimestamp).apply(lambda x: x.date())]

        elif self.timestamp_format == TimestampFormat.MULTI_COLUMN_DATE:
            datetime_series = series.apply(datetime.datetime.fromtimestamp)

            year_series = datetime_series.apply(lambda x: x.year)
            month_series = datetime_series.apply(lambda x: x.month)
            day_series = datetime_series.apply(lambda x: x.day)

            formatted_series = [year_series, month_series, day_series,]

        else:
            raise NotImplementedError(f"Timestamp format {self.timestamp_format} not implemented.")

        return formatted_series

    @staticmethod
    def partial_sort(
        list_: List[Any],
        p: float,
    ):
        """Partially sort a list.
        
        Args:
            list_: The list to partially sort.
            p: A number between 0 and 1 indicating how sorted the list should be. 0 means completely random, 1 means completely sorted.
        """

        sorted_list = sorted(list_)
        random_list = sorted_list.copy()
        random.shuffle(random_list)

        n = len(list_)
        n_sorted = int(n * p)
        n_random = n - n_sorted

        partially_sorted_lst = sorted_list[:n_sorted] + random_list[n_sorted:]
        random.shuffle(partially_sorted_lst)

        return pd.Series(partially_sorted_lst)

    @staticmethod
    def get_column_names(timestamp_format: TimestampFormat) -> List[str]:
        """Get the column names for a timestamp format."""

        if timestamp_format == TimestampFormat.UNIX_EPOCH:
            return ["timestamp"]
        
        elif timestamp_format == TimestampFormat.ISO_8601:
            return ["timestamp"]
        
        elif timestamp_format == TimestampFormat.SINGLE_COLUMN_TIMESTAMP:
            return ["timestamp"]
        
        elif timestamp_format == TimestampFormat.MULTI_COLUMN_TIMESTAMP:
            return ["date", "time"]
        
        elif timestamp_format == TimestampFormat.SINGLE_COLUMN_DATE:
            return ["date"]

        elif timestamp_format == TimestampFormat.MULTI_COLUMN_DATE:
            return ["year", "month", "day"]

        else:
            raise NotImplementedError(f"Timestamp format {timestamp_format} not implemented.")