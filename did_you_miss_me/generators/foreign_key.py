from typing import Any, Optional

import pandas as pd

from did_you_miss_me.generators.column import (
    ColumnGenerator,
)

### Foreign Keys ###

class ForeignKeyGenerator(ColumnGenerator):

    @classmethod
    def create(
        cls,
        name: Optional[str] = None,
    ) -> "ForeignKeyGenerator":
        """Create a ForeignKeyGenerator."""

        return cls(
            name=name,
        )

    def generate(self, num_rows:int ) -> pd.Series:
        return pd.Series(range(num_rows))
