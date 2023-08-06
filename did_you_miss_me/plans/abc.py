from pydantic import BaseModel
from abc import ABC
from typing import Any

### ABCs ###


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

class MissingnessModifier(DataModifier, ABC):
    """
    Abstract base class for DataModifiers that add missingness to data.
    """

    pass

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