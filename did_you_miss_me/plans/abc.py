from pydantic import BaseModel
from abc import ABC
from typing import Any

### ABCs ###


class Plan(BaseModel, ABC):
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

    This behavior is recursive. For example, if you create a MultibatchPlan with no arguments, it will create a list of EpochPlans with no arguments, which will create a list of DataFramePlans with no arguments, which will create a list of SeriesPlans with no arguments, which will create a list of ColumnPlans with no arguments.

    Plans are designed to be immutable. Once you create a Plan, you cannot change it.

    Plans are designed to be serializable. You can convert a Plan to a dictionary using the .to_dict() method, and you can convert a dictionary to a Plan using the .from_dict() method.
    """

    pass


class DataGenerator(Plan, ABC):
    """
    Abstract class for generator plans.
    """

    def generate(
        self,
        *args,
        **kwargs,
    ) -> Any:

        raise NotImplementedError


class MissingnessPlan(Plan, ABC):
    """
    Abstract class for missingness plans.
    """

    pass