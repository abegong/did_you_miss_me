from enum import Enum

from did_you_miss_me.plans.abc import (
    GenerationPlan,
    MissingnessPlan,
    GenerationAndMissingnessPlan,
)


class ColumnGenerationPlan(GenerationPlan):
    name: str  # The name of the column
    faker_type: str  # The type of data to generate


class ColumnMissingnessType(str, Enum):
    ALWAYS = "ALWAYS"
    NEVER = "NEVER"
    PROPORTIONAL = "PROPORTIONAL"
    # CONDITIONAL = "CONDITIONAL"


class ColumnMissingnessPlan(MissingnessPlan):
    missingness_type: ColumnMissingnessType  # The type of missingness to include


class ProportionalColumnMissingnessPlan(ColumnMissingnessPlan):
    proportion: float


# @dataclass
# class ConditionalColumnMissingnessPlan(ColumnMissingnessPlan):
#     conditional_column_name : str
#     proportions : Dict


class ColumnPlan(
    ColumnGenerationPlan, ColumnMissingnessPlan, GenerationAndMissingnessPlan
):
    pass


class ProportionalColumnPlan(
    ColumnPlan,
    ColumnGenerationPlan,
    ProportionalColumnMissingnessPlan,
    GenerationAndMissingnessPlan,
):
    pass


# @dataclass
# class ConditionalColumnPlan(ColumnGenerationPlan, ConditionalColumnMissingnessPlan):
#     pass
