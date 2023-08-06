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

    All Plan classes inherit from this abstract class.

    __init__ methods for each Plan class follow a similar pattern:
    * You can construct the object directly from a dictionary, or
    * pass in keyword arguments which are used to create the Plan.
        
    If you use the keyword argument approach, the Plan will be created with random values using sensible defaults for ranges.
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


class ColumnMissingnessType(str, Enum):
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
class ProportionalColumnPlan(ColumnPlan, ColumnGenerationPlan, ProportionalColumnMissingnessPlan):
    pass


# @dataclass
# class ConditionalColumnPlan(ColumnGenerationPlan, ConditionalColumnMissingnessPlan):
#     pass


### Dataframe-level Plan classes ###

class DataframeRowGenerationPlan(BaseModel):
    num_rows: Optional[int]
    min_rows: Optional[int]
    max_rows: Optional[int]

    def __init__(
        self,
        num_rows: Optional[int] = None,
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None,
    ):
        has_min_max = (min_rows is not None) and (max_rows is not None)
        
        if min_rows is None and max_rows is not None:
            raise ValueError("If you specify max_rows, you must also specify min_rows.")
        
        elif min_rows is not None and max_rows is None:
            raise ValueError("If you specify min_rows, you must also specify max_rows.")

        if num_rows is None and not has_min_max:
            if random.random() < 0.5:
                num_rows = random.randint(100, 500)
            else:
                min_rows = random.randint(50, 400)
                max_rows = random.randint(min_rows, min_rows + 100)
        
        elif num_rows is not None and has_min_max:
            raise ValueError("You cannot specify both num_rows and min_rows/max_rows.")

        super().__init__(
            num_rows=num_rows,
            min_rows=min_rows,
            max_rows=max_rows,
        )

class DataframeGenerationPlan(BaseModel):
    column_plans : List[ColumnGenerationPlan]
    row_plan : DataframeRowGenerationPlan

    @property
    def num_columns(self):
        return len(self.column_plans)

    def __init__(
        self,
        column_plans: Optional[List[ColumnGenerationPlan]] = None,
        row_plan: Optional[DataframeRowGenerationPlan] = None,
        num_rows: Optional[int] = None,
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None,
        num_columns: Optional[int] = None,
    ):
        if column_plans is None:
            if num_columns is None:
                num_columns = 12

            column_plans = []
            for i in range(num_columns):

                            
                column_plan = ColumnGenerationPlan(
                    name=f"column_{i + 1}",
                    faker_type=random.choice(FAKER_TYPES),    
                )
                # generate_column_plan(column_index=i + 1)
                column_plans.append(column_plan)
        
        if row_plan is None:
            row_plan = DataframeRowGenerationPlan(
                num_rows=num_rows,
                min_rows=min_rows,
                max_rows=max_rows,
            )
        
        super().__init__(
            column_plans=column_plans,
            row_plan=row_plan,
        )


class DataframeMissingnessPlan(BaseModel):
    column_plans : List[ColumnMissingnessPlan]

    @property
    def num_columns(self):
        return len(self.column_plans)

    def __init__(
        self,
        column_plans: Optional[List[ColumnMissingnessPlan]] = None,
        num_columns: Optional[int] = None,
    ):
        if column_plans is None:
            if num_columns is None:
                num_columns = 12

            column_plans = []
            for i in range(num_columns):
                column_plan = self._generate_column_plan()
                column_plans.append(column_plan)
        
        super().__init__(
            column_plans=column_plans,
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

class DataframePlan(BaseModel):
    column_plans: List[ColumnPlan]
    row_plan : DataframeRowGenerationPlan

    def __init__(
        self,
        column_plans: Optional[List[ColumnPlan]] = None,
        row_plan: Optional[DataframeRowGenerationPlan] = None,
        generation_plan: Optional[DataframeGenerationPlan] = None,
        missingness_plan: Optional[DataframeMissingnessPlan] = None,
        num_columns: Optional[int] = None,
        num_rows: Optional[int] = None,
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None,
    ):
        if column_plans is None:
            if generation_plan is None and missingness_plan is None:
                if num_columns is None:
                    num_columns = 12

                if row_plan is None:
                    row_plan = DataframeRowGenerationPlan(
                        num_rows=num_rows,
                        min_rows=min_rows,
                        max_rows=max_rows,
                    )
                
                generation_plan = DataframeGenerationPlan(
                    num_columns=num_columns,
                    num_rows=num_rows,
                )
                missingness_plan = DataframeMissingnessPlan(
                    num_columns=num_columns,
                )

            elif generation_plan is None:
                if row_plan is None:
                    row_plan = DataframeRowGenerationPlan(
                        num_rows=num_rows,
                        min_rows=min_rows,
                        max_rows=max_rows,
                    )

                generation_plan = DataframeGenerationPlan(
                    num_columns=missingness_plan.num_columns,
                    num_rows=num_rows,
                )
            
            elif missingness_plan is None:
                missingness_plan = DataframeMissingnessPlan(
                    num_columns=generation_plan.num_columns,
                )

                row_plan = generation_plan.row_plan
        
            else:
                assert generation_plan.num_columns == missingness_plan.num_columns

            column_plans = []
            for i in range(generation_plan.num_columns):
                column_plan = self._generate_column_plan(
                    generation_plan.column_plans[i],
                    missingness_plan.column_plans[i],
                )
                column_plans.append(column_plan)
        
        else:
            if row_plan is None:
                row_plan = DataframeRowGenerationPlan(
                    num_rows=num_rows,
                    min_rows=min_rows,
                    max_rows=max_rows,
                )
            
        super().__init__(
            column_plans=column_plans,
            row_plan=row_plan,
        )

    @staticmethod
    def _generate_column_plan(
        column_generation_plan: ColumnGenerationPlan,
        column_missingness_plan: ColumnMissingnessPlan,
    ) -> ColumnMissingnessPlan:
        
        missingness_type = column_missingness_plan.missingness_type

        if missingness_type == "ALWAYS":
            return ColumnPlan(
                name=column_generation_plan.name,
                missingness_type=missingness_type,
                faker_type=column_generation_plan.faker_type,
            )

        elif missingness_type == "NEVER":
            return ColumnPlan(
                name=column_generation_plan.name,
                missingness_type=missingness_type,
                faker_type=column_generation_plan.faker_type,
            )

        elif missingness_type == "PROPORTIONAL":
            return ProportionalColumnPlan(
                name=column_generation_plan.name,
                missingness_type=missingness_type,
                faker_type=column_generation_plan.faker_type,
                proportion=column_missingness_plan.proportion,
            )

### Epoch and Multibatch Plan classes ###

class EpochPlan(BaseModel):
    dataframe_plan : DataframePlan
    num_batches : int

    def __init__(
        self,
        dataframe_plan: Optional[DataframePlan] = None,
        generation_plan: Optional[DataframeGenerationPlan] = None,
        num_batches: Optional[int] = None,
    ):                        
        if num_batches is None:
            num_batches = int(random.uniform(0,10) ** 2)

        if dataframe_plan is None:

            if generation_plan is None:
                generation_plan = DataframeGenerationPlan()
        
            dataframe_plan = DataframePlan(
                generation_plan=generation_plan,
            )

        super().__init__(
            dataframe_plan=dataframe_plan,
            num_batches=num_batches,
        )

class MultiBatchPlan(BaseModel):
    epochs : List[EpochPlan]

    @property
    def num_epochs(self):
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

            num_epochs = random.randint(3, 6)
            epochs = [EpochPlan(
                generation_plan=generation_plan,
            ) for _ in range(num_epochs)]

        super().__init__(
            epochs=epochs,
            **kwargs
        )
