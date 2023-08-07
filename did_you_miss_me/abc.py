from pydantic import BaseModel
from abc import ABC
from typing import Any


class DataTool(BaseModel, ABC):
    """
    Abstract base class for DataGenerators and DataModifiers.
    """

    @classmethod
    def create(
        cls,
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
