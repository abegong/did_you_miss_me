import pandas as pd

from missingness_data_generator.plan_generators import generate_column_plan
from missingness_data_generator.series_generators import generate_series_from_plan

def generate_series(
        
) -> pd.Series:
    
    plan = generate_column_plan(
        column_index=1
    )
    series = generate_series_from_plan(
        n=200,
        plan=plan,
    )

    return series
