from typing import Dict, List
from enum import Enum
from pydantic.dataclasses import dataclass
from abc import ABC

### ABCs ###

@dataclass
class Plan(ABC):
    """
    Abstract class for plans.

    There are two types of plans: generator plans and missingness plans.
    Generator plans are used to generate data, and missingness plans are used to
    add missingness ("missify") data.

    Plans can be applied to dataframes, series.
    """
    pass

@dataclass
class GeneratorPlan(Plan, ABC):
    """
    Abstract class for generator plans.
    """
    pass

@dataclass
class MissingnessPlan(Plan, ABC):
    """
    Abstract class for missingness plans.
    """
    pass

### Column-level Plan classes ###

@dataclass
class ColumnGenerationPlan(Plan):
    name : str                                  # The name of the column
    faker_type : str                            # The type of data to generate

class ColumnMissingnessType(Enum):
    ALWAYS = "ALWAYS"
    NEVER = "NEVER"
    PROPORTIONAL = "PROPORTIONAL"
    # CONDITIONAL = "CONDITIONAL"

@dataclass
class ColumnMissingnessPlan(MissingnessPlan):
    missingness_type : ColumnMissingnessType    # The type of missingness to include

@dataclass
class ProportionalColumnMissingnessPlan(ColumnMissingnessPlan):
    proportion : float

# @dataclass
# class ConditionalColumnMissingnessPlan(ColumnMissingnessPlan):
#     conditional_column_name : str
#     proportions : Dict

@dataclass
class ColumnPlan(ColumnGenerationPlan, ColumnMissingnessPlan):
    pass

@dataclass
class ProportionalColumnPlan(ColumnGenerationPlan, ProportionalColumnMissingnessPlan):
    pass

# @dataclass
# class ConditionalColumnPlan(ColumnGenerationPlan, ConditionalColumnMissingnessPlan):
#     pass






# @dataclass
# class DataframePlan:
#     columns = List[ColumnPlan]

# @dataclass
# class EpochPlan:
#     dataframe_plan = List[DataframePlan]
#     num_batches = int

# @dataclass
# class MultibatchPlan:
#     epochs = List[EpochPlan]
#     index_columns #???
