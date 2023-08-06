import random
from typing import List, Optional
from enum import Enum
from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from abc import ABC

from did_you_miss_me.faker_types import (
    FAKER_TYPES,
)

### ABCs ###

@dataclass
class Plan(ABC):
    """
    Abstract class for plans.

    There are two types of plans: generator plans and missingness plans.
    Generator plans are used to generate data, and missingness plans are used to
    add missingness ("missify") data.

    Plans can be applied to series, dataframes, epochs, and multibatches.

    * A Series is a 1-dimensional array of data.
    * A DataFrame is a 2-dimensional array of data. (A pandas DataFrame, essentially.)
    * An Epoch is a list of DataFrames with the same Plans for generation and missingness.
    * A Multibatch is a list of Epochs.
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
    name: str  # The name of the column
    faker_type: str  # The type of data to generate


class ColumnMissingnessType(Enum):
    ALWAYS = "ALWAYS"
    NEVER = "NEVER"
    PROPORTIONAL = "PROPORTIONAL"
    # CONDITIONAL = "CONDITIONAL"


@dataclass
class ColumnMissingnessPlan(MissingnessPlan):
    missingness_type: ColumnMissingnessType  # The type of missingness to include


@dataclass
class ProportionalColumnMissingnessPlan(ColumnMissingnessPlan):
    proportion: float


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


### Dataframe-level Plan classes ###

class DataframeGenerationPlan(BaseModel):
    column_plans : List[ColumnGenerationPlan]
    num_rows : int #!!! Extend this to allow for different numbers of rows per dataframe

    def __init__(
        self,
        column_plans: Optional[List[ColumnGenerationPlan]] = None,
        num_rows: Optional[int] = None,
    ):
        if column_plans is None:
            n_columns = 12

            column_plans = []
            for i in range(n_columns):

                            
                column_plan = ColumnGenerationPlan(
                    name=f"column_{i + 1}",
                    faker_type=random.choice(FAKER_TYPES),    
                )
                # generate_column_plan(column_index=i + 1)
                column_plans.append(column_plan)
        
        if num_rows is None:
            num_rows = random.randint(100, 500)
        
        print(column_plans)

        super().__init__(
            column_plans=column_plans,
            num_rows=num_rows,
        )

class DataframeMissingnessPlan(BaseModel):
    columns : List[ColumnMissingnessPlan]

    def __init__(
        self,
        columns: Optional[List[ColumnMissingnessPlan]] = None,
    ):
        if columns is None:
            columns = []
            for i in range(12):
                column_plan = self._generate_column_plan()
                columns.append(column_plan)
        
        super().__init__(
            columns=columns,
        )

    @staticmethod
    def _generate_column_plan(
        missingness_type: Optional[ColumnMissingnessType] = None,
    ) -> ColumnMissingnessPlan:
        
        if missingness_type is None:
            missingness_type = random.choice([
                ColumnMissingnessType.NEVER,
                ColumnMissingnessType.NEVER,
                ColumnMissingnessType.NEVER,
                ColumnMissingnessType.NEVER,
                ColumnMissingnessType.PROPORTIONAL,
                ColumnMissingnessType.PROPORTIONAL,
                ColumnMissingnessType.ALWAYS,
                # "CONDITIONAL",
            ])

        if missingness_type == ColumnMissingnessType.ALWAYS:
            return ColumnMissingnessPlan(
                missingness_type=missingness_type,
            )

        elif missingness_type == ColumnMissingnessType.NEVER:
            return ColumnMissingnessPlan(
                missingness_type=missingness_type,
            )

        elif missingness_type == ColumnMissingnessType.PROPORTIONAL:
            # A little math to make most proportions close to 0 or 1, with "close to 0" being more likely
            proportion = random.random() ** 3
            if random.random() < 0.25:
                proportion = 1 - proportion

            return ProportionalColumnMissingnessPlan(
                missingness_type=missingness_type, proportion=proportion
            )
        
### Epoch and Multibatch Plan classes ###

class EpochPlan(BaseModel):
    generation_plan : DataframeGenerationPlan
    missingness_plan : DataframeMissingnessPlan
    num_batches : int

    def __init__(
        self,
        generation_plan: Optional[DataframeGenerationPlan] = None,
        missingness_plan: Optional[DataframeMissingnessPlan] = None,
        num_batches: Optional[int] = None,
    ):
        if generation_plan is None:
            generation_plan = DataframeGenerationPlan()
        
        if missingness_plan is None:
            missingness_plan = DataframeMissingnessPlan()
        
        if num_batches is None:
            num_batches = random.randint(3, 6)

        super().__init__(
            generation_plan=generation_plan,
            missingness_plan=missingness_plan,
            num_batches=num_batches,
        )

class MultiBatchPlan(BaseModel):
    epochs : List[EpochPlan]

    @property
    def n_epochs(self):
        return len(self.epochs)

    def __init__(
        self,
        epochs: Optional[List[EpochPlan]] = None,
        **kwargs,
    ):
        if epochs is None:

            # By default, all epochs have the same generation plan; only the missingness plans vary.
            # As a result, we need a generation plan, which will be shared across all epochs.
            generation_plan = DataframeGenerationPlan()
            print("Here")

            n_epochs = random.randint(3, 6)
            epochs = [EpochPlan(
                generation_plan=generation_plan,
            ) for _ in range(n_epochs)]

        super().__init__(
            epochs=epochs,
            **kwargs
        )
