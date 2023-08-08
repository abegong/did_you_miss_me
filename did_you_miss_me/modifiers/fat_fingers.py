from abc import ABC
from enum import Enum
import random
from typing import Optional
from pydantic import BaseModel, Field

import pandas as pd

from did_you_miss_me.abc import (
    DataModifier,
)


class ColumnMissingnessType(str, Enum):
    ALWAYS = "ALWAYS"
    NEVER = "NEVER"
    PROPORTIONAL = "PROPORTIONAL"
    # CONDITIONAL = "CONDITIONAL"


WEIGHTED_MISSINGNESS_TYPES = [
    "NEVER",
    "NEVER",
    "NEVER",
    "NEVER",
    "PROPORTIONAL",
    "PROPORTIONAL",
    "ALWAYS",
    # "CONDITIONAL",
]


class ColumnMissingnessParams(BaseModel):
    pass


class ProportionalColumnMissingnessParams(ColumnMissingnessParams):
    proportion: float


class FatFingersModifier(DataModifier, ABC):
    """Abstract base class for DataModifiers that add typos to data

    Common typos include:
    - Missing characters
    - Extra characters
    - Transposed characters
    - Mistaken characters
    - Repeated characters
    """

    pass


class ColumnFatFingersModifier(FatFingersModifier):
    error_rate: float = Field(
        default=0.01,
        description="The probability that any given value will be modified",
    )
    include_missing_chars: bool = Field(
        default=True,
        description="Whether to include missing characters as a possible error",
    )
    include_extra_chars: bool = Field(
        default=True,
        description="Whether to include extra characters as a possible error",
    )
    include_transposed_chars: bool = Field(
        default=True,
        description="Whether to include transposed characters as a possible error",
    )
    include_mistaken_chars: bool = Field(
        default=True,
        description="Whether to include mistaken characters as a possible error",
    )
    include_repeated_chars: bool = Field(
        default=True,
        description="Whether to include repeated characters as a possible error",
    )

    @classmethod
    def create(
        cls,
        error_rate: Optional[float] = None,
    ):
        if error_rate is None:
            error_rate = 0.01

        return cls(
            error_rate=error_rate,
        )

    def modify(
        self,
        series: pd.Series,
    ) -> pd.Series:
        """Modify a series of data with typos"""

        new_series = series.copy()

        for i, value in series.items():
            if random.random() < self.error_rate:
                new_series[i] = self._modify_value(
                    value,
                    self._get_random_error_type(),
                )

        return new_series

    @property
    def possible_errors(self):
        possible_errors = []
        if self.include_missing_chars:
            possible_errors.append("missing_chars")

        if self.include_extra_chars:
            possible_errors.append("extra_chars")

        if self.include_transposed_chars:
            possible_errors.append("transposed_chars")

        if self.include_mistaken_chars:
            possible_errors.append("mistaken_chars")

        if self.include_repeated_chars:
            possible_errors.append("repeated_chars")

        return possible_errors

    def _get_random_error_type(self):
        return random.choice(self.possible_errors)

    @staticmethod
    def _modify_value(
        value: str,
        error_type: str,
    ) -> str:
        """Modify a single value with typos"""

        if error_type == "missing_chars":
            # Drop a random character from the string
            k = random.randint(0, len(value) - 1)
            modified_value = value[:k] + value[k + 1 :]

        elif error_type == "extra_chars":
            # Add a random character to the string
            k = random.randint(0, len(value) - 1)
            modified_value = value[:k] + random.choice(list(value)) + value[k:]

        elif error_type == "transposed_chars":
            # Transpose two random characters in the string
            k = random.randint(0, len(value) - 2)
            modified_value = value[:k] + value[k + 1] + value[k] + value[k + 2 :]

        elif error_type == "mistaken_chars":
            # Replace a random character in the string with a random character in the alphabet
            k = random.randint(0, len(value) - 1)
            modified_value = (
                value[:k]
                + random.choice(list("abcdefghijklmnopqrstuvwxyz1234567890"))
                + value[k + 1 :]
            )

        elif error_type == "repeated_chars":
            # Repeat a random character in the string
            k = random.randint(0, len(value) - 1)
            modified_value = value[:k] + value[k] + value[k:]

        return modified_value


# class DataframeFatFingersModifier(FatFingersModifier):

#     @classmethod
#     def modify(
#         cls,
#         df: pd.DataFrame,
#     ) -> pd.DataFrame:
#         """Modify a dataframe of data with typos"""

#         create

#         new_df = df.copy()
#         for column in df.columns:
#             new_df[column] = self._modify_column(df[column])

#         return new_df

#     def _modify_column(

# column_modifiers: List[ColumnFatFingersModifier]

# @property
# def num_columns(self):
#     return len(self.column_modifiers)

# @classmethod
# def create(
#     cls,
#     column_generators: Optional[List[ColumnMissingnessModifier]] = None,
#     num_columns: Optional[int] = None,
# ):
#     if column_generators is None:
#         if num_columns is None:
#             num_columns = 12

#         column_modifiers = []
#         for i in range(num_columns):
#             column_modifier = cls._generate_column_generator()
#             column_modifiers.append(column_modifier)

#     return cls(
#         column_modifiers=column_modifiers,
#     )

# @staticmethod
# def _generate_column_generator(
#     missingness_type: Optional[ColumnMissingnessType] = None,
# ) -> ColumnMissingnessModifier:
#     if missingness_type is None:
#         missingness_type = random.choice(
#             [
#                 ColumnMissingnessType.NEVER,
#                 ColumnMissingnessType.NEVER,
#                 ColumnMissingnessType.NEVER,
#                 ColumnMissingnessType.NEVER,
#                 ColumnMissingnessType.PROPORTIONAL,
#                 ColumnMissingnessType.PROPORTIONAL,
#                 ColumnMissingnessType.ALWAYS,
#                 # "CONDITIONAL",
#             ]
#         )

#     if missingness_type == ColumnMissingnessType.ALWAYS:
#         return ColumnMissingnessModifier(
#             missingness_type=missingness_type,
#         )

#     elif missingness_type == ColumnMissingnessType.NEVER:
#         return ColumnMissingnessModifier(
#             missingness_type=missingness_type,
#         )

#     elif missingness_type == ColumnMissingnessType.PROPORTIONAL:
#         # A little math to make most proportions close to 0 or 1, with "close to 0" being more likely
#         proportion = random.random() ** 3
#         if random.random() < 0.25:
#             proportion = 1 - proportion

#         return ColumnMissingnessModifier(
#             missingness_type=missingness_type,
#             missingness_params=ProportionalColumnMissingnessParams(
#                 proportion=proportion,
#             ),
#         )
