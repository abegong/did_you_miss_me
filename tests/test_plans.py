"""Tests that verify that Plan objects work as expected: constructors, serialization, etc."""

import json
import pytest
import random


from did_you_miss_me.generators.multibatch import (
    MissingFakerEpochGenerator,
    MissingFakerMultiBatchGenerator,
)
from did_you_miss_me.generators.dataframe import (
    MissingFakerDataframeGenerator,
)


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(40)


def test__dataframe_generator():
    # This is just a smoke test to make sure that the generator can be constructed.
    generator = MissingFakerDataframeGenerator.create()
    print(json.dumps(generator.model_dump(), indent=2))


def test__epoch_generator():
    # This is just a smoke test to make sure that the generator can be constructed.
    generator = MissingFakerEpochGenerator.create(
        num_batches=3,
        # min_rows=10,
        # max_rows=20,
    )
    print(json.dumps(generator.model_dump(), indent=2))


def test__multi_batch_generator():
    # This is just a smoke test to make sure that the generator can be constructed.
    generator = MissingFakerMultiBatchGenerator.create()
    print(json.dumps(generator.model_dump(), indent=2))


def test__pydantic_foo_bar():
    import random
    from pydantic import BaseModel, Field

    class A(BaseModel):
        foo: int = Field(default_factory=lambda: random.randint(0, 100))

        # def __init__(
        #     self,
        #     foo: Optional[str] = None,
        #     *args,
        #     **kwargs,
        # ):
        #     if foo is None:
        #         foo = random.randint(0, 100)

        #     super().__init__(foo=foo)

    class B(A):
        bar: int = Field(default_factory=lambda: random.randint(0, 100))

        # def __init__(
        #     self,
        #     foo: Optional[str] = None,
        #     bar: Optional[str] = None,
        # ):
        #     if bar is None:
        #         bar = random.randint(0, 100)

        #     super().__init__(foo=foo)

    a = A()
    print(a)

    a = A(foo=10)
    print(a)

    b = B()
    print(b)
    # assert b.foo == 100
