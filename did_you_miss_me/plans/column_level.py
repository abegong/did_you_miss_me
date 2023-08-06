from enum import Enum
from faker import Faker
import random
from typing import Optional
from pydantic import BaseModel, Field

import pandas as pd

from did_you_miss_me.plans.abc import (
    DataGenerator,
    MissingnessModifier,
)
from did_you_miss_me.faker_types import FAKER_TYPES

class ColumnGenerator(DataGenerator):
    pass

class FakerColumnGenerator(ColumnGenerator):
    name: str = Field(
        default_factory=lambda: f"column_{random.randint(0, 1000000)}",
        description="The name of the column"
    )
    faker_type: str = Field(
        default_factory=lambda: random.choice(FAKER_TYPES),
        description="The name of the faker method to call to generate column values."
    )

    _fake = Faker()

    def generate_faker_value(self, faker_type: str):
        """Generate a value from the faker library.

        Args:
            faker_type: The name of the faker method to call.
        """
        method = getattr(self._fake, faker_type)
        value = method()
        return value


    def generate(self, n: int) -> pd.Series:
        """Generate a series of random data

        Args:
            n: The number of rows to generate.
        """

        series = pd.Series([self.generate_faker_value(self.faker_type) for i in range(n)])

        return series


class ColumnMissingnessType(str, Enum):
    ALWAYS = "ALWAYS"
    NEVER = "NEVER"
    PROPORTIONAL = "PROPORTIONAL"
    # CONDITIONAL = "CONDITIONAL"


WEIGHTED_MISSINGNESS_TYPES = [
    "NEVER",
    "NEVER",
    "NEVER",
    "NEVER",
    "PROPORTIONAL",
    "PROPORTIONAL",
    "ALWAYS",
    # "CONDITIONAL",
]

class ColumnMissingnessParams(BaseModel):
    pass

class ProportionalColumnMissingnessParams(ColumnMissingnessParams):
    proportion: float

# class ConditionalColumnMissingnessParams(ColumnMissingnessParams):
#     conditional_column_name : str
#     proportions : Dict

class ColumnMissingnessModifier(MissingnessModifier):
    missingness_type: ColumnMissingnessType = Field(
        default_factory=lambda: random.choice(WEIGHTED_MISSINGNESS_TYPES),
        description="The type of missingness to include"
    )
    missingness_params: Optional[ColumnMissingnessParams] = Field(
        None,
        description="Parameters for the missingness type"
    )

    @classmethod
    def create(
        cls,
        missingness_type: Optional[ColumnMissingnessType] = None,
        missingness_params: Optional[ColumnMissingnessParams] = None,
    ):
        if missingness_type is None:
            missingness_type = random.choice(WEIGHTED_MISSINGNESS_TYPES)

        if missingness_params is None:
            if missingness_type == "PROPORTIONAL":
                missingness_params = ProportionalColumnMissingnessParams(
                    proportion=random.random()
                )

        return cls(
            missingness_type=missingness_type,
            missingness_params=missingness_params,
        )


class MissingFakerColumnGenerator(FakerColumnGenerator, ColumnMissingnessModifier):

    @classmethod
    def create(
        cls,
        name: Optional[str] = None,
        faker_type: Optional[str] = None,
        missingness_type: Optional[ColumnMissingnessType] = None,
        missingness_params: Optional[ColumnMissingnessParams] = None,
    ):
        if name is None:
            name = f"column_{random.randint(0, 1000000)}"
        
        if faker_type is None:
            faker_type = random.choice(FAKER_TYPES)

        if missingness_type is None:
            missingness_type = random.choice(WEIGHTED_MISSINGNESS_TYPES)

        if missingness_params is None:
            if missingness_type == "PROPORTIONAL":
                missingness_params = ProportionalColumnMissingnessParams(
                    proportion=random.random()
                )

            # elif missingness_type == "CONDITIONAL":
            #     missingness_params = ConditionalColumnMissingnessParams(
            #         conditional_column_name = "column_0",
            #         proportions = {
            #             "value_1" : 0.5,
            #             "value_2" : 0.5,
            #         }
            #     )

        return cls(
            name=name,
            faker_type=faker_type,
            missingness_type=missingness_type,
            missingness_params=missingness_params,
        )