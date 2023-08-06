import os

def _load_faker_types():
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "faker_types.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as f:
        faker_types = f.read().split("\n")

    return faker_types

FAKER_TYPES = _load_faker_types()