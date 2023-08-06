from enum import Enum
from faker import Faker
import random
from typing import Any, Optional
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

    def _generate_faker_value(self, faker_type: str):
        """Generate a value from the faker library.

        Args:
            faker_type: The name of the faker method to call.
        """
        method = getattr(self._fake, faker_type)
        value = method()
        return value


    def generate(self, num_rows: int) -> pd.Series:
        """Generate a series of random data

        Args:
            num_rows: The number of rows to generate.
        """

        series = pd.Series([self._generate_faker_value(self.faker_type) for i in range(num_rows)])

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
    
    def modify(
        self,
        series: pd.Series,
    ) -> pd.Series:

        if self.missingness_type == ColumnMissingnessType.ALWAYS:
            new_series = pd.Series([None for i in range(len(series))])

        elif self.missingness_type == ColumnMissingnessType.NEVER:
            new_series = series.copy()

        elif self.missingness_type == ColumnMissingnessType.PROPORTIONAL:
            z = pd.Series([random.random() < self.missingness_params.proportion for i in range(len(series))])
            new_series = series.copy()
            new_series[z] = None
            return new_series

        else:
            raise ValueError(f"Unrecognized missingness type: {self.missingness_type}")

        return new_series


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
    
    def generate(
        self,
        num_rows: int,
        add_missingness: bool = True,
    ) -> pd.Series:
        series = super().generate(num_rows=num_rows)

        if add_missingness:
            modified_series = self.modify(series)
        else:
            modified_series = series

        return modified_series