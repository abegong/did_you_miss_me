import random
from typing import Dict, Tuple
import os

from missingness_data_generator.plans import (
    ColumnPlan,
    ProportionallyMissingColumnPlan,
)

# def generate_random_missingness_type_and_kwargs() -> Tuple[str, Dict]:
#     type_ = random.choice([
#         "always",
#         "never",
#         "proportionally",
#     ])

#     if type_ == "always":
#         kwargs = {}

#     elif type_ == "never":
#         kwargs = {}
    
#     elif type_ == "proportionally":
#         kwargs = {
#             "proportion" : random.random()
#         }

#     return type_, kwargs

def _load_faker_types():
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "faker_types.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as f:
        faker_types = f.read().split("\n")

    return faker_types

FAKER_TYPES = _load_faker_types()
MISSINGNESS_TYPES = [
    "always",
    "never",
    "proportionally",
    # "conditionally",
]
# Add a weight to each missingness type to make some more likely than others
WEIGHTED_MISSINGNESS_TYPES = [
    "never", "never", "never", "never",
    "proportionally", "proportionally",
    "always",
    # "conditionally",
]

def generate_column_plan(column_index) -> Tuple[str, Dict]:
    missingness_type = random.choice(WEIGHTED_MISSINGNESS_TYPES)
    faker_type = random.choice(FAKER_TYPES)

    if missingness_type == "always":
        return ColumnPlan(
            name=f"column_{column_index}",
            missingness_type=missingness_type,
            faker_type=faker_type,
        )

    elif missingness_type == "never":
        return ColumnPlan(
            name=f"column_{column_index}",
            missingness_type=missingness_type,
            faker_type=faker_type,
        )
    
    elif missingness_type == "proportionally":
        # A little math to make most proportions close to 0 or 1, with "close to 0" being more likely
        proportion = random.random()**3
        if random.random() < 0.25:
            proportion = 1 - proportion


        return ProportionallyMissingColumnPlan(
            name=f"column_{column_index}",
            missingness_type=missingness_type,
            faker_type=faker_type,
            proportion=proportion
        )