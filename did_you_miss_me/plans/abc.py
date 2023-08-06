from pydantic import BaseModel
from abc import ABC
from typing import Any

### ABCs ###


class DataTool(BaseModel, ABC):
    """
    All Plan classes inherit from this abstract class.

    __init__ methods for each Plan class follow a similar pattern:
    * You can construct the object directly from a dictionary, or
    * pass in keyword arguments which are used to create the Plan.

    If you use the keyword argument approach, the Plan will be created with random values using sensible defaults for ranges.

    This behavior is recursive. For example, if you create a MultibatchPlan with no arguments, it will create a list of EpochGenerators with no arguments, which will create a list of DataFramePlans with no arguments, which will create a list of SeriesPlans with no arguments, which will create a list of ColumnPlans with no arguments.
    """

    pass


class DataGenerator(DataTool, ABC):
    """
    Abstract class for generator plans.
    """

    def generate(
        self,
        *args,
        **kwargs,
    ) -> Any:

        raise NotImplementedError


class DataModifier(DataTool, ABC):
    """
    Abstract class for missingness plans.
    """

    def modify(
        self,
        *args,
        **kwargs,
    ) -> Any:

        raise NotImplementedError

class MissingnessModifier(DataModifier, ABC):
    """
    Abstract class for missingness plans.
    """

    pass