# import random
# import pandas as pd
# from faker import Faker

# from did_you_miss_me.plans import (
#     ColumnMissingnessType,
#     FakerColumnGenerator,
#     MissingFakerColumnGenerator,
#     ColumnMissingnessModifier,
# )

# _fake = Faker()


# def missify_series_from_plan(
#     series: pd.Series,
#     plan: ColumnMissingnessModifier,
# ) -> pd.Series:
#     """Add missingness to a series according to a plan."""

#     if plan.missingness_type == ColumnMissingnessType.ALWAYS:
#         new_series = pd.Series([None for i in range(len(series))])

#     elif plan.missingness_type == ColumnMissingnessType.NEVER:
#         new_series = series.copy()

#     elif plan.missingness_type == ColumnMissingnessType.PROPORTIONAL:
#         z = pd.Series([random.random() < plan.missingness_params.proportion for i in range(len(series))])
#         new_series = series.copy()
#         new_series[z] = None
#         return new_series

#     else:
#         raise ValueError(f"Unrecognized missingness type: {plan.missingness_type}")

#     return new_series
