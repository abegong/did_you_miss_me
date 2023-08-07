from abc import ABC
from enum import Enum
import random
from typing import Any, List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4

import pandas as pd

from did_you_miss_me.abc import (
    DataGenerator,
)
from did_you_miss_me.generators.column import (
    ColumnGenerator,
)

### Primary Keys ###

class PrimaryKeyType(str, Enum):
    """Types of primary keys"""

    integer = "INTEGER"
    uuid4 = "UUID4"

class PrimaryKeyParams(BaseModel, ABC):
    """Parameters for generating a primary key."""
    pass

class IntegerPrimaryKeyParams(PrimaryKeyParams):
    """Parameters for generating an ascending integer primary key."""

    digits: int = Field(
        random.randint(4, 10),
        description="The number of digits to use when generating integer-type keys.",
    )
    ascending: bool = Field(
        True,
        description="Whether to generate an ascending or unsorted integer primary key.",
    )
    data_type: str = Field(
        "int",
        description="The data type of the primary key.",
    )
    pad_with_zeros: Optional[bool] = Field(
        False,
        description="Whether to pad the primary key with zeros. (Only used when data_type is 'str'.)",
    )

class PrimaryKeyColumnGenerator(ColumnGenerator):
    """Specifies how to create a column containing a primary key."""

    key_type: PrimaryKeyType = Field(
        random.choice(list(PrimaryKeyType)),
        description="The type of primary key to generate.",
    )
    key_params: Optional[PrimaryKeyParams] = Field(
        None,
        description="Parameters for generating the primary key.",
    )

    @classmethod
    def create(
        cls,
        name: Optional[str] = None,
        key_type: Optional[PrimaryKeyType] = None,
        ascending: Optional[bool] = True,
        digits: Optional[int] = None,
        data_type: Optional[str] = None,
        pad_with_zeros: Optional[bool] = None,
    ) -> Any:
        """Create a PrimaryKeyColumnGenerator."""

        if name is None:
            name = "primary_key_column"

        if key_type is None:
            key_type = random.choice(list(PrimaryKeyType))

        if key_type == PrimaryKeyType.integer:
            if digits is None:
                digits = random.randint(4, 10)

            if data_type is None:
                data_type = random.choice(["int", "str"])

            if data_type == "str":
                if pad_with_zeros is None:
                    pad_with_zeros = random.random() < 0.5
            
            key_params = IntegerPrimaryKeyParams(
                digits=digits,
                ascending=ascending,
                data_type=data_type,
                pad_with_zeros=pad_with_zeros,
            )

        else:
            key_params = None

        return cls(
            name=name,
            key_type=key_type,
            key_params=key_params,
        )
    
    def generate(
        self,
        num_rows:int,
        starting_value: Optional[int] = 0,
        seed: Optional[int] = None,
    ) -> pd.Series:
        """Generate a column containing a primary key."""

        if seed is not None:
            random.seed(seed)
    
        if self.key_type == PrimaryKeyType.integer:
            print(self.key_params)

            if self.key_params.ascending:
                series = pd.Series(range(starting_value, starting_value + num_rows))
            
            else:
                series = pd.Series([random.randint(0, 10 ** self.key_params.digits) for _ in range(num_rows)])
            
            if self.key_params.data_type == "str":
                if self.key_params.pad_with_zeros:
                    series = series.astype(str).str.zfill(self.key_params.digits)
                else:
                    series = series.astype(str)

            return series
    
        elif self.key_type == PrimaryKeyType.uuid4:
            return pd.Series([str(uuid4()) for _ in range(num_rows)])        
    