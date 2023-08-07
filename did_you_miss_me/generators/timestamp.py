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

    unix_epoch = "UNIX_EPOCH"
    iso_8601 = "ISO_8601"
    single_column_timestamp = "SINGLE_COLUMN_TIMESTAMP"
    multi_column_timestamp = "MULTI_COLUMN_TIMESTAMP"
    single_column_date = "SINGLE_COLUMN_DATE"
    multi_column_date = "MULTI_COLUMN_DATE"

class TimestampColumnGenerator(MultiColumnGenerator):

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

    def generate(self, num_rows:int) -> List[pd.Series]:
        """Generate a timestamp column."""

        # Create a series of random timestamps
        series = pd.Series([random.randint(self.start_time, self.end_time) for _ in range(num_rows)])

        # Sort the series, at least partially
        sortedish_series = self.partial_sort(series, self.sortedness)

        # Format the series, depending on the timestamp format
        if self.timestamp_format == TimestampFormat.unix_epoch:
            formatted_series = [sortedish_series]
        
        elif self.timestamp_format == TimestampFormat.iso_8601:
            formatted_series = [sortedish_series.apply(datetime.datetime.fromtimestamp)]
        
        elif self.timestamp_format == TimestampFormat.single_column_timestamp:
            formatted_series = [sortedish_series.apply(datetime.datetime.fromtimestamp).apply(str)]
        
        elif self.timestamp_format == TimestampFormat.multi_column_timestamp:
            date_series = sortedish_series.apply(datetime.datetime.fromtimestamp)
            time_series = sortedish_series.apply(lambda x: datetime.timedelta(seconds=x))

            formatted_series = [date_series, time_series]
        
        elif self.timestamp_format == TimestampFormat.single_column_date:
            formatted_series = [sortedish_series.apply(datetime.datetime.fromtimestamp).apply(lambda x: x.date())]

        elif self.timestamp_format == TimestampFormat.multi_column_date:
            day_series = sortedish_series.apply(datetime.datetime.fromtimestamp).apply(lambda x: x.date())
            month_series = sortedish_series.apply(lambda x: x // (3600*24*30))
            year_series = sortedish_series.apply(lambda x: x // (3600*24*365))

            formatted_series = [day_series, month_series, year_series]

        else:
            raise NotImplementedError(f"Timestamp format {self.timestamp_format} not implemented.")

        return dict(zip(self.names, formatted_series))

    @staticmethod
    def partial_sort(lst, p):
        sorted_lst = sorted(lst)
        random_lst = sorted_lst.copy()
        random.shuffle(random_lst)

        n = len(lst)
        n_sorted = int(n * p)
        n_random = n - n_sorted

        partially_sorted_lst = sorted_lst[:n_sorted] + random_lst[n_sorted:]
        random.shuffle(partially_sorted_lst)

        return pd.Series(partially_sorted_lst)

    @staticmethod
    def get_column_names(timestamp_format: TimestampFormat) -> List[str]:
        """Get the column names for a timestamp format."""

        if timestamp_format == TimestampFormat.unix_epoch:
            return ["timestamp"]
        
        elif timestamp_format == TimestampFormat.iso_8601:
            return ["timestamp"]
        
        elif timestamp_format == TimestampFormat.single_column_timestamp:
            return ["timestamp"]
        
        elif timestamp_format == TimestampFormat.multi_column_timestamp:
            return ["date", "time"]
        
        elif timestamp_format == TimestampFormat.single_column_date:
            return ["date"]

        elif timestamp_format == TimestampFormat.multi_column_date:
            return ["day", "month", "year"]

        else:
            raise NotImplementedError(f"Timestamp format {timestamp_format} not implemented.")