from pydantic import BaseModel
from abc import ABC
from typing import Any


class DataTool(BaseModel, ABC):
    """
    Abstract base class for DataGenerators and DataModifiers.
    """

    def create(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError

### DataGenerators ###

class DataGenerator(DataTool, ABC):
    """
    Abstract base class for DataGenerators
    """

    def generate(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError


class EpochGenerator(DataGenerator, ABC):
    """
    Abstract base class for EpochGenerators
    """

    pass


class MultiBatchGenerator(DataGenerator, ABC):
    """
    Abstract base class for MultiBatchGenerators
    """

    pass


### DataModifiers ###

class DataModifier(DataTool, ABC):
    """
    Abstract base class for DataModifiers
    """

    def modify(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
