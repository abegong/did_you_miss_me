from abc import ABC
from faker import Faker
import random
from typing import Any, Dict, List, Optional
from pydantic import Field

import pandas as pd

from did_you_miss_me.abc import (
    DataGenerator,
)
from did_you_miss_me.modifiers.missingness import (
    ColumnMissingnessType,
    ColumnMissingnessParams,
    ColumnMissingnessModifier,
    WEIGHTED_MISSINGNESS_TYPES,
    ProportionalColumnMissingnessParams,
)
from did_you_miss_me.faker_types import FAKER_TYPES


class ColumnGenerator(DataGenerator, ABC):
    """
    Abstract base class for ColumnGenerators
    """

    name: str = Field(
        default_factory=lambda: f"column_{random.randint(0, 1000000)}",
        description="The name of the column",
    )

    def generate(self, *args, **kwargs) -> pd.Series:
        raise NotImplementedError

class MultiColumnGenerator(DataGenerator, ABC):
    """Abstract base class for generators that create multiple columns."""

    names: List[str] = Field(
        default_factory=lambda: [f"column_{random.randint(0, 1000000)}"],
        description="The names of the columns",
    )

    @property
    def num_columns(self) -> int:
        return len(self.names)
    
    def generate(self, *args, **kwargs) -> Dict[str, pd.Series]:
        raise NotImplementedError



class FakerColumnGenerator(ColumnGenerator):
    faker_type: str = Field(
        default_factory=lambda: random.choice(FAKER_TYPES),
        description="The name of the faker method to call to generate column values.",
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

        series = pd.Series(
            [self._generate_faker_value(self.faker_type) for i in range(num_rows)]
        )

        return series


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
