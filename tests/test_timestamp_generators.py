"""Tests that verify that Plan objects work as expected: constructors, serialization, etc."""

import datetime
import json
import pytest
import random


from did_you_miss_me.generators.timestamp import (
    TimestampMultiColumnGenerator,
    TimestampFormat,
)


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)


def test__timestamp_multi_column_generator():
    generator = TimestampMultiColumnGenerator.create()
    values = generator.generate(
        num_rows=5,
    )
    print(values)


def test__timestamp_multi_column_generator__with_unix_epoch_format():
    generator = TimestampMultiColumnGenerator.create(
        timestamp_format=TimestampFormat.UNIX_EPOCH,
        start_time=int(datetime.datetime(2023,1,1).timestamp()),
        end_time=int(datetime.datetime(2023,1,31).timestamp()),
    )
    values = generator.generate(
        num_rows=5,
    )
    print(values["column_timestamp"])
    assert list(values["column_timestamp"]) == [
        1672689973,
        1673421827,
        1673740981,
        1674754100,
        1673585221,
    ]


def test__timestamp_multi_column_generator__with_iso_8601_format():
    generator = TimestampMultiColumnGenerator.create(
        timestamp_format=TimestampFormat.ISO_8601,
        start_time=int(datetime.datetime(2023,1,1).timestamp()),
        end_time=int(datetime.datetime(2023,1,31).timestamp()),
    )
    values = generator.generate(
        num_rows=5,
    )
    print(values["column_timestamp"])
    assert [str(x) for x in list(values["column_timestamp"])] == [
        "2023-01-02 13:06:13",
        "2023-01-11 00:23:47",
        "2023-01-14 17:03:01",
        "2023-01-26 10:28:20",
        "2023-01-12 21:47:01",
    ]

def test__timestamp_multi_column_generator__with_single_column_timestamp_format():
    generator = TimestampMultiColumnGenerator.create(
        timestamp_format=TimestampFormat.SINGLE_COLUMN_TIMESTAMP,
        start_time=int(datetime.datetime(2023,1,1).timestamp()),
        end_time=int(datetime.datetime(2023,1,31).timestamp()),
    )
    values = generator.generate(
        num_rows=5,
    )
    print(values["column_timestamp"])
    assert list(values["column_timestamp"]) == [
        "2023-01-02 13:06:13",
        "2023-01-11 00:23:47",
        "2023-01-14 17:03:01",
        "2023-01-26 10:28:20",
        "2023-01-12 21:47:01",
    ]

def test__timestamp_multi_column_generator__with_multi_column_timestamp_format():
    generator = TimestampMultiColumnGenerator.create(
        timestamp_format=TimestampFormat.MULTI_COLUMN_TIMESTAMP,
        start_time=int(datetime.datetime(2023,1,1).timestamp()),
        end_time=int(datetime.datetime(2023,1,31).timestamp()),
    )
    values = generator.generate(
        num_rows=5,
    )
    print(values["column_date"])
    assert [str(x) for x in list(values["column_date"])] == [
        "2023-01-02",
        "2023-01-11",
        "2023-01-14",
        "2023-01-26",
        "2023-01-12",
    ]
    print(values["column_time"])
    assert [str(x) for x in list(values["column_time"])] == [
        "13:06:13",
        "00:23:47",
        "17:03:01",
        "10:28:20",
        "21:47:01",
    ]

def test__timestamp_multi_column_generator__with_single_column_date_format():
    generator = TimestampMultiColumnGenerator.create(
        timestamp_format=TimestampFormat.SINGLE_COLUMN_DATE,
        start_time=int(datetime.datetime(2023,1,1).timestamp()),
        end_time=int(datetime.datetime(2023,1,31).timestamp()),
    )
    values = generator.generate(
        num_rows=5,
    )
    print(values["column_date"])
    assert [str(x) for x in list(values["column_date"])] == [
        "2023-01-02",
        "2023-01-11",
        "2023-01-14",
        "2023-01-26",
        "2023-01-12",
    ]

def test__timestamp_multi_column_generator__with_multi_column_date_format():
    generator = TimestampMultiColumnGenerator.create(
        timestamp_format=TimestampFormat.MULTI_COLUMN_DATE,
        start_time=int(datetime.datetime(2023,1,1).timestamp()),
        end_time=int(datetime.datetime(2023,1,31).timestamp()),
    )
    values = generator.generate(
        num_rows=5,
    )
    print(values["column_year"])
    assert list(values["column_year"]) == [
        2023,
        2023,
        2023,
        2023,
        2023,
    ]
    print(values["column_month"])
    assert list(values["column_month"]) == [
        1,
        1,
        1,
        1,
        1,
    ]
    print(values["column_day"])
    assert list(values["column_day"]) == [
        2,
        11,
        14,
        26,
        12,
    ]

def test__partial_sort():
    list_ = list(range(10))
    
    partially_sorted_list = list(TimestampMultiColumnGenerator._partial_sort(list_, 1.0))
    assert partially_sorted_list == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    partially_sorted_list = list(TimestampMultiColumnGenerator._partial_sort(list_, 0.0))
    print(partially_sorted_list)
    assert partially_sorted_list == [8, 1, 7, 2, 4, 3, 5, 0, 9, 6]

    partially_sorted_list = list(TimestampMultiColumnGenerator._partial_sort(list_, 0.7))
    print(partially_sorted_list)
    assert partially_sorted_list == [1, 4, 2, 5, 6, 7, 8, 3, 9, 0]
