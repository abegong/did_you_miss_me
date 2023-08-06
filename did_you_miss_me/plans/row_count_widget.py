import random
from pydantic import BaseModel
from typing import Optional

class RowCountWidget(BaseModel):
    """Specifies how many rows should be generated

    * If exact_rows is specified, then that number of rows will be generated.
    * Otherwise, if min_rows and max_rows are specified, then a random number of rows
    between min_rows and max_rows will be generated.
    """

    exact_rows: Optional[int]
    min_rows: Optional[int]
    max_rows: Optional[int]

    @property
    def num_rows(self):
        if self.exact_rows is not None:
            return self.exact_rows
        else:
            return random.randint(self.min_rows, self.max_rows)

    @classmethod
    def create(
        cls,
        exact_rows: Optional[int] = None,
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None,
    ):
        has_min_max = (min_rows is not None) and (max_rows is not None)

        if min_rows is None and max_rows is not None:
            raise ValueError("If you specify max_rows, you must also specify min_rows.")

        elif min_rows is not None and max_rows is None:
            raise ValueError("If you specify min_rows, you must also specify max_rows.")

        if exact_rows is None and not has_min_max:
            if random.random() < 0.5:
                exact_rows = random.randint(100, 500)
            else:
                min_rows = random.randint(50, 400)
                max_rows = random.randint(min_rows, min_rows + 100)

        elif exact_rows is not None and has_min_max:
            raise ValueError(
                "You cannot specify both exact_rows and min_rows/max_rows."
            )

        return cls(
            exact_rows=exact_rows,
            min_rows=min_rows,
            max_rows=max_rows,
        )