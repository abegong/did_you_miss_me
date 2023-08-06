from abc import ABC
from enum import Enum
from faker import Faker
import random
from typing import Optional
from pydantic import BaseModel, Field

import pandas as pd

from did_you_miss_me.plans.abc import (
    DataModifier,
)
from did_you_miss_me.faker_types import FAKER_TYPES

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


class MissingnessModifier(DataModifier, ABC):
    """
    Abstract base class for DataModifiers that add missingness to data.
    """

    pass


class ColumnMissingnessModifier(MissingnessModifier):
    missingness_type: ColumnMissingnessType = Field(
        default_factory=lambda: random.choice(WEIGHTED_MISSINGNESS_TYPES),
        description="The type of missingness to include",
    )
    missingness_params: Optional[ColumnMissingnessParams] = Field(
        None, description="Parameters for the missingness type"
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
            z = pd.Series(
                [
                    random.random() < self.missingness_params.proportion
                    for i in range(len(series))
                ]
            )
            new_series = series.copy()
            new_series[z] = None
            return new_series

        else:
            raise ValueError(f"Unrecognized missingness type: {self.missingness_type}")

        return new_series

