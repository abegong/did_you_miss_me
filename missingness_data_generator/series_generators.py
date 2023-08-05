import random
import pandas as pd
from faker import Faker

from missingness_data_generator.plans import (
    ColumnMissingnessType,
    # ColumnPlan,
    ColumnGenerationPlan,
    ColumnMissingnessPlan,
)

_fake = Faker()


def generate_faker_value(faker_type: str):
    """Generate a value from the faker library.

    Args:
        faker_type: The name of the faker method to call.
    """
    method = getattr(_fake, faker_type)
    value = method()
    return value


def generate_series_from_plan(n: int, plan: ColumnGenerationPlan) -> pd.Series:
    """Generate a series of random data according to a plan.

    Note: This function does not add missingness to the series. To do that, use `missify_series_from_plan`.

    Args:
        n: The number of rows to generate.
        plan: The plan to use to generate the series.
    """

    series = pd.Series([generate_faker_value(plan.faker_type) for i in range(n)])

    return series


def missify_series_from_plan(
    series: pd.Series,
    plan: ColumnMissingnessPlan,
) -> pd.Series:
    """Add missingness to a series according to a plan."""

    if plan.missingness_type == ColumnMissingnessType.ALWAYS:
        new_series = pd.Series([None for i in range(len(series))])

    elif plan.missingness_type == ColumnMissingnessType.NEVER:
        new_series = series.copy()

    elif plan.missingness_type == ColumnMissingnessType.PROPORTIONAL:
        z = pd.Series([random.random() < plan.proportion for i in range(len(series))])
        new_series = series.copy()
        new_series[z] = None
        return new_series

    else:
        raise ValueError(f"Unrecognized missingness type: {plan.missingness_type}")

    return new_series
