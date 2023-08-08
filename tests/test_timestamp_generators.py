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
    random.seed(40)
    generator = TimestampMultiColumnGenerator.create(
        timestamp_format=TimestampFormat.UNIX_EPOCH,
        start_time=int(datetime.datetime(2023,1,1).timestamp()),
        end_time=int(datetime.datetime(2023,1,31).timestamp()),
    )
    values = generator.generate(
        num_rows=5,
        seed=40,
    )
    print(values["timestamp"])
    assert list(values["timestamp"]) == [
        1673585221,
        1674479935,
        1672689973,
        1673585221,
        1674479935,
    ]


def test__timestamp_multi_column_generator__with_iso_8601_format():
    generator = TimestampMultiColumnGenerator.create(
        timestamp_format=TimestampFormat.ISO_8601,
        start_time=int(datetime.datetime(2023,1,1).timestamp()),
        end_time=int(datetime.datetime(2023,1,31).timestamp()),
    )
    values = generator.generate(
        num_rows=5,
        seed=40,
    )
    print(values["timestamp"])
    assert [str(x) for x in list(values["timestamp"])] == [
        "2023-01-12 21:47:01",
        "2023-01-23 06:18:55",
        "2023-01-02 13:06:13",
        "2023-01-12 21:47:01",
        "2023-01-23 06:18:55",
    ]

def test__timestamp_multi_column_generator__with_single_column_timestamp_format():
    generator = TimestampMultiColumnGenerator.create(
        timestamp_format=TimestampFormat.SINGLE_COLUMN_TIMESTAMP,
        start_time=int(datetime.datetime(2023,1,1).timestamp()),
        end_time=int(datetime.datetime(2023,1,31).timestamp()),
    )
    values = generator.generate(
        num_rows=5,
        seed=40,
    )
    print(values["timestamp"])
    assert list(values["timestamp"]) == [
        "2023-01-12 21:47:01",
        "2023-01-23 06:18:55",
        "2023-01-02 13:06:13",
        "2023-01-12 21:47:01",
        "2023-01-23 06:18:55",
    ]

def test__timestamp_multi_column_generator__with_multi_column_timestamp_format():
    generator = TimestampMultiColumnGenerator.create(
        timestamp_format=TimestampFormat.MULTI_COLUMN_TIMESTAMP,
        start_time=int(datetime.datetime(2023,1,1).timestamp()),
        end_time=int(datetime.datetime(2023,1,31).timestamp()),
    )
    values = generator.generate(
        num_rows=5,
        seed=40,
    )
    print(values["date"])
    assert [str(x) for x in list(values["date"])] == [
        "2023-01-12",
        "2023-01-23",
        "2023-01-02",
        "2023-01-12",
        "2023-01-23",
    ]
    print(values["time"])
    assert [str(x) for x in list(values["time"])] == [
        "21:47:01",
        "06:18:55",
        "13:06:13",
        "21:47:01",
        "06:18:55",
    ]

def test__timestamp_multi_column_generator__with_single_column_date_format():
    generator = TimestampMultiColumnGenerator.create(
        timestamp_format=TimestampFormat.SINGLE_COLUMN_DATE,
        start_time=int(datetime.datetime(2023,1,1).timestamp()),
        end_time=int(datetime.datetime(2023,1,31).timestamp()),
    )
    values = generator.generate(
        num_rows=5,
        seed=40,
    )
    print(values["date"])
    assert [str(x) for x in list(values["date"])] == [
        "2023-01-12",
        "2023-01-23",
        "2023-01-02",
        "2023-01-12",
        "2023-01-23",
    ]

def test__timestamp_multi_column_generator__with_multi_column_date_format():
    generator = TimestampMultiColumnGenerator.create(
        timestamp_format=TimestampFormat.MULTI_COLUMN_DATE,
        start_time=int(datetime.datetime(2023,1,1).timestamp()),
        end_time=int(datetime.datetime(2023,1,31).timestamp()),
    )
    values = generator.generate(
        num_rows=5,
        seed=40,
    )
    print(values["year"])
    assert list(values["year"]) == [
        2023,
        2023,
        2023,
        2023,
        2023,
    ]
    print(values["month"])
    assert list(values["month"]) == [
        1,
        1,
        1,
        1,
        1,
    ]
    print(values["day"])
    assert list(values["day"]) == [
        12,
        23,
        2,
        12,
        23,
    ]