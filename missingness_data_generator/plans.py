from typing import Dict, List
from pydantic.dataclasses import dataclass

@dataclass
class ColumnPlan:
    name : str
    faker_type : str
    missingness_type : str #Switch this for an enum

@dataclass
class ProportionallyMissingColumnPlan(ColumnPlan):
    proportion : float

@dataclass
class ConditionallyMissingColumnPlan(ColumnPlan):
    conditional_column_name : str
    proportions : Dict

@dataclass
class DataframePlan:
    columns = List[ColumnPlan]

@dataclass
class EpochPlan:
    dataframe_plan = List[DataframePlan]
    num_batches = int

# @dataclass
# class MultibatchPlan:
#     epochs = List[EpochPlan]
#     index_columns #???
