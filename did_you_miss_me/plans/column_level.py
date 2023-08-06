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

    # def __init__(
    #     self,
    #     name: Optional[str] = None,
    #     faker_type: Optional[str] = None,
    #     *args,
    #     **kwargs,
    # ):
    #     if name is None:
    #         name = f"column_{random.randint(0, 1000000)}"
        
    #     if faker_type is None:
    #         faker_type = random.choice(FAKER_TYPES)

    #     super().__init__(
    #         name=name,
    #         faker_type=faker_type,
    #     )


    def generate_faker_value(self, faker_type: str):
        """Generate a value from the faker library.

        Args:
            faker_type: The name of the faker method to call.
        """
        method = getattr(self._fake, faker_type)
        value = method()
        return value


    def generate(self, n: int) -> pd.Series:
        """Generate a series of random data according to a plan.

        Note: This function does not add missingness to the series. To do that, use `missify_series_from_plan`.

        Args:
            n: The number of rows to generate.
            plan: The plan to use to generate the series.
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

def _create_missingness_param(missingness_type: ColumnMissingnessType):
    if missingness_type == "PROPORTIONAL":
        return ProportionalColumnMissingnessParams(
            proportion=random.random()
        )

    # elif missingness_type == "CONDITIONAL":
    #     return ConditionalColumnMissingnessParams(
    #         conditional_column_name = random.choice(WEIGHTED_MISSINGNESS_TYPES)
    #     )

    return None

class ColumnMissingnessModifier(MissingnessModifier):
    missingness_type: Optional[ColumnMissingnessType] = Field(
        default_factory=lambda: random.choice(WEIGHTED_MISSINGNESS_TYPES),
        description="The type of missingness to include"
    )
    missingness_params: Optional[ColumnMissingnessParams] = None
    # Field(
    #     default_factory=lambda: _create_missingness_param(self.missingness_type),
    #     description="Parameters for the missingness type"
    # )

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
            # elif missingness_type == "CONDITIONAL":
            #     missingness_params = ConditionalColumnMissingnessParams(
            #         conditional_column_name = random.choice(WEIGHTED_MISSINGNESS_TYPES)
            #       )

    #     super().__init__(
    #         missingness_type=missingness_type,
    #         missingness_params=missingness_params,
    #     )

class MissingFakerColumnGenerator(FakerColumnGenerator):
    name: str  # The name of the column
    faker_type: str  # The type of data to generate
    missingness_type: ColumnMissingnessType  # The type of missingness to include
    missingness_params: Optional[ColumnMissingnessParams] = None  # Parameters for the missingness type

    def __init__(
        self,
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

        super().__init__(
            name=name,
            faker_type=faker_type,
            missingness_type=missingness_type,
            missingness_params=missingness_params,
        )