import random
import pandas as pd
from faker import Faker

from missingness_data_generator.plans import (
    ColumnMissingnessType,
    ColumnPlan,
    ColumnMissingnessPlan,
)

_fake = Faker()


def generate_faker_value(faker_type: str):
    method = getattr(_fake, faker_type)
    value = method()
    return value


def generate_always_missing_series(n: int) -> pd.Series:
    return pd.Series([None for i in range(n)])


def generate_never_missing_series(
    n: int,
    faker_type: str,
) -> pd.Series:
    return pd.Series([generate_faker_value(faker_type) for i in range(n)])


def generate_proportionally_missing_series(
    n: int,
    faker_type: str,
    proportion: float,
) -> pd.Series:
    series = pd.Series([generate_faker_value(faker_type) for i in range(n)])
    missingness = pd.Series([random.random() for i in range(n)])
    series[missingness < proportion] = None

    return series


def generate_series_from_plan(n: int, plan: ColumnPlan) -> pd.Series:
    if plan.missingness_type == ColumnMissingnessType.ALWAYS:
        series = generate_always_missing_series(
            n=n,
        )

    elif plan.missingness_type == ColumnMissingnessType.NEVER:
        series = generate_never_missing_series(n=n, faker_type=plan.faker_type)

    elif plan.missingness_type == ColumnMissingnessType.PROPORTIONAL:
        series = generate_proportionally_missing_series(
            n=n,
            faker_type=plan.faker_type,
            proportion=plan.proportion,
        )

    else:
        raise ValueError(f"Unrecognized missingness type: {plan.missingness_type}")

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
