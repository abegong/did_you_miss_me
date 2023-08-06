from enum import Enum
import random
from typing import Optional
from pydantic import BaseModel

from did_you_miss_me.plans.abc import (
    GenerationPlan,
    MissingnessPlan,
    GenerationAndMissingnessPlan,
)
from did_you_miss_me.faker_types import FAKER_TYPES

class ColumnGenerationPlan(GenerationPlan):
    name: str  # The name of the column
    faker_type: str  # The type of data to generate

    def __init__(
        self,
        name: Optional[str] = None,
        faker_type: Optional[str] = None,
    ):
        if name is None:
            name = f"column_{random.randint(0, 1000000)}"
        
        if faker_type is None:
            faker_type = random.choice(FAKER_TYPES)

        super().__init__(
            name=name,
            faker_type=faker_type,
        )

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

class ColumnMissingnessPlan(MissingnessPlan):
    missingness_type: ColumnMissingnessType  # The type of missingness to include
    missingness_params: Optional[ColumnMissingnessParams] = None  # Parameters for the missingness type

    def __init__(
        self,
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

            # elif missingness_type == "CONDITIONAL":
            #     missingness_params = ConditionalColumnMissingnessParams(
            #         conditional_column_name = random.choice(WEIGHTED_MISSINGNESS_TYPES)
            #       )

        super().__init__(
            missingness_type=missingness_type,
            missingness_params=missingness_params,
        )

class ColumnPlan(GenerationAndMissingnessPlan):
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

# class ProportionalColumnMissingnessPlan(ColumnMissingnessPlan):
#     proportion: float


# class ProportionalColumnPlan(
#     ColumnPlan,
#     ColumnGenerationPlan,
#     ProportionalColumnMissingnessPlan,
#     GenerationAndMissingnessPlan,
# ):
#     pass

# class ConditionalColumnMissingnessPlan(ColumnMissingnessPlan):
#     conditional_column_name : str
#     proportions : Dict


# class ConditionalColumnPlan(ColumnGenerationPlan, ConditionalColumnMissingnessPlan):
#     pass
