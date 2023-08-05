import random
from typing import Dict, Optional, Tuple
import os

from missingness_data_generator.plans import (
    ColumnPlan,
    ColumnMissingnessPlan,
    ProportionalColumnMissingnessPlan,
    ProportionalColumnPlan
)

def _load_faker_types():
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "faker_types.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as f:
        faker_types = f.read().split("\n")

    return faker_types

FAKER_TYPES = _load_faker_types()
MISSINGNESS_TYPES = [
    "ALWAYS",
    "NEVER",
    "PROPORTIONAL",
    # "CONDITIONAL",
]
# Add a weight to each missingness type to make some more likely than others
WEIGHTED_MISSINGNESS_TYPES = [
    "NEVER", "NEVER", "NEVER", "NEVER",
    "PROPORTIONAL", "PROPORTIONAL",
    "ALWAYS",
    # "CONDITIONAL",
]

def generate_column_plan(
    column_index: int,
    missingness_type: Optional[str] = None,
) -> Tuple[str, Dict]:
    
    if missingness_type is None:
        missingness_type = random.choice(WEIGHTED_MISSINGNESS_TYPES)
    
    faker_type = random.choice(FAKER_TYPES)

    if missingness_type == "ALWAYS":
        return ColumnPlan(
            name=f"column_{column_index}",
            missingness_type=missingness_type,
            faker_type=faker_type,
        )

    elif missingness_type == "NEVER":
        return ColumnPlan(
            name=f"column_{column_index}",
            missingness_type=missingness_type,
            faker_type=faker_type,
        )
    
    elif missingness_type == "PROPORTIONAL":
        # A little math to make most proportions close to 0 or 1, with "close to 0" being more likely
        proportion = random.random()**3
        if random.random() < 0.25:
            proportion = 1 - proportion

        return ProportionalColumnPlan(
            name=f"column_{column_index}",
            missingness_type=missingness_type,
            faker_type=faker_type,
            proportion=proportion
        )

def generate_column_missingness_plan(
    column_index: int,
    missingness_type: Optional[str] = None,
) -> Tuple[str, Dict]:
    if missingness_type is None:
        missingness_type = random.choice(WEIGHTED_MISSINGNESS_TYPES)

    if missingness_type == "ALWAYS":
        return ColumnMissingnessPlan(
            missingness_type=missingness_type,
        )

    elif missingness_type == "NEVER":
        return ColumnMissingnessPlan(
            missingness_type=missingness_type,
        )
    
    elif missingness_type == "PROPORTIONAL":
        # A little math to make most proportions close to 0 or 1, with "close to 0" being more likely
        proportion = random.random()**3
        if random.random() < 0.25:
            proportion = 1 - proportion

        return ProportionalColumnMissingnessPlan(
            missingness_type=missingness_type,
            proportion=proportion
        )