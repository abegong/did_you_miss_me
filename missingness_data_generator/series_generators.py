import random
import pandas as pd
from faker import Faker

from missingness_data_generator.plans import ColumnPlan

_fake = Faker()

def generate_faker_value(faker_type:str):
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
    series[missingness<proportion] = None

    return series

# def generate_series_from_missingness_type_and_kwargs(
#     n: int,
#     missingness_type: str,
#     missingness_kwargs
# ) -> pd.Series:

#     if missingness_type == "always":
#         series = generate_always_missing_series(n)

#     elif missingness_type == "never":
#         series = generate_never_missing_series(n)

#     elif missingness_type == "proportionally":
#         print(missingness_kwargs)
#         series = generate_proportionally_missing_series(
#             n=n,
#             proportion=missingness_kwargs["proportion"]
#         )

#     return series

def generate_series_from_plan(
    n: int,
    plan: ColumnPlan
) -> pd.Series:
    print(plan)
    print(plan.missingness_type)

    if plan.missingness_type == "always":
        series = generate_always_missing_series(
            n=n,
        )

    elif plan.missingness_type == "never":
        series = generate_never_missing_series(
            n=n,
            faker_type=plan.faker_type
        )

    elif plan.missingness_type == "proportionally":
        series = generate_proportionally_missing_series(
            n=n,
            faker_type=plan.faker_type,
            proportion=plan.proportion,
        )

    else:
        print(plan.missingness_type)

    return series