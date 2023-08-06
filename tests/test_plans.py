"""Tests that verify that Plan objects work as expected: constructors, serialization, etc."""

import json
import pytest
import random


from did_you_miss_me.plans import (
    ColumnGenerationPlan, #noqa: F401
    ColumnMissingnessPlan, #noqa: F401
    ProportionalColumnMissingnessPlan, #noqa: F401
    # ConditionalColumnMissingnessPlan,
    ColumnPlan, #noqa: F401
    ProportionalColumnPlan, #noqa: F401
    # DataframeGenerationPlan,
    # DataframeMissingnessPlan,
    DataframePlan,
    EpochPlan,
    MultiBatchPlan,
)


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)


def test__dataframe_plan():
    plan = DataframePlan()
    print(json.dumps(plan.model_dump(), indent=2))


def test__epoch_plan():
    plan = EpochPlan(
        num_batches=3,
        # min_rows=10,
        # max_rows=20,
    )
    # print(plan.model_dump_json())
    print(json.dumps(plan.model_dump(), indent=2))

    # assert plan.model_dump() == {}
    # assert plan.model_dump_json() == {}


def test__multi_batch_plan():
    plan = MultiBatchPlan()
    # print(plan.model_dump_json())
    print(json.dumps(plan.model_dump(), indent=2))

    # assert plan.model_dump() == {}
    # assert plan.model_dump_json() == {}
