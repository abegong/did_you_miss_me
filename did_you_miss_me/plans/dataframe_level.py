import random
from pydantic import BaseModel
from typing import List, Optional

import pandas as pd

from did_you_miss_me.faker_types import (
    FAKER_TYPES,
)
from did_you_miss_me.plans.abc import (
    DataGenerator,
    MissingnessModifier,
)
from did_you_miss_me.plans.column_level import (
    ColumnGenerator,
    FakerColumnGenerator,
    MissingFakerColumnGenerator,
    ColumnMissingnessType,
    ColumnMissingnessModifier,
    ProportionalColumnMissingnessParams,
)


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
            raise ValueError("You cannot specify both exact_rows and min_rows/max_rows.")

        return cls(
            exact_rows=exact_rows,
            min_rows=min_rows,
            max_rows=max_rows,
        )


class DataframeGenerator(DataGenerator):
    column_generators: List[ColumnGenerator]
    row_plan: RowCountWidget

    @property
    def num_columns(self):
        return len(self.column_generators)

    @property
    def num_rows(self):
        return self.row_plan.num_rows

    @classmethod
    def create(
        cls,
        column_generators: Optional[List[ColumnGenerator]] = None,
        row_plan: Optional[RowCountWidget] = None,
        exact_rows: Optional[int] = None,
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None,
        num_columns: Optional[int] = None,
    ):
        if column_generators is None:
            if num_columns is None:
                num_columns = 12

            column_generators = []
            for i in range(num_columns):
                column_generator = FakerColumnGenerator(
                    name=f"column_{i + 1}",
                    faker_type=random.choice(FAKER_TYPES),
                )
                # generate_column_generator(column_index=i + 1)
                column_generators.append(column_generator)

        if row_plan is None:
            row_plan = RowCountWidget(
                exact_rows=exact_rows,
                min_rows=min_rows,
                max_rows=max_rows,
            )

        return cls(
            column_generators=column_generators,
            row_plan=row_plan,
        )


class DataframeMissingnessModifier(MissingnessModifier):
    column_modifiers: List[ColumnMissingnessModifier]

    @property
    def num_columns(self):
        return len(self.column_modifiers)

    @classmethod
    def create(
        cls,
        column_generators: Optional[List[ColumnMissingnessModifier]] = None,
        num_columns: Optional[int] = None,
    ):
        if column_generators is None:
            if num_columns is None:
                num_columns = 12

            column_modifiers = []
            for i in range(num_columns):
                column_modifier = cls._generate_column_generator()
                column_modifiers.append(column_modifier)

        return cls(
            column_modifiers=column_modifiers,
        )

    @staticmethod
    def _generate_column_generator(
        missingness_type: Optional[ColumnMissingnessType] = None,
    ) -> ColumnMissingnessModifier:
        if missingness_type is None:
            missingness_type = random.choice(
                [
                    ColumnMissingnessType.NEVER,
                    ColumnMissingnessType.NEVER,
                    ColumnMissingnessType.NEVER,
                    ColumnMissingnessType.NEVER,
                    ColumnMissingnessType.PROPORTIONAL,
                    ColumnMissingnessType.PROPORTIONAL,
                    ColumnMissingnessType.ALWAYS,
                    # "CONDITIONAL",
                ]
            )

        if missingness_type == ColumnMissingnessType.ALWAYS:
            return ColumnMissingnessModifier(
                missingness_type=missingness_type,
            )

        elif missingness_type == ColumnMissingnessType.NEVER:
            return ColumnMissingnessModifier(
                missingness_type=missingness_type,
            )

        elif missingness_type == ColumnMissingnessType.PROPORTIONAL:
            # A little math to make most proportions close to 0 or 1, with "close to 0" being more likely
            proportion = random.random() ** 3
            if random.random() < 0.25:
                proportion = 1 - proportion

            return ColumnMissingnessModifier(
                missingness_type=missingness_type,
                missingness_params=ProportionalColumnMissingnessParams(
                    proportion=proportion,
                ),
            )


class MissingFakerDataframeGenerator(DataGenerator):
    column_generators: List[MissingFakerColumnGenerator]
    row_plan: RowCountWidget

    @property
    def num_rows(self):
        return self.row_plan.num_rows

    @classmethod
    def create(
        cls,
        column_generators: Optional[List[ColumnGenerator]] = None,
        row_plan: Optional[RowCountWidget] = None,
        generation_plan: Optional[DataframeGenerator] = None,
        missingness_plan: Optional[DataframeMissingnessModifier] = None,
        num_columns: Optional[int] = None,
        exact_rows: Optional[int] = None,
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None,
    ):
        if column_generators is None:
            if generation_plan is None and missingness_plan is None:
                if num_columns is None:
                    num_columns = 12

                if row_plan is None:
                    row_plan = RowCountWidget(
                        exact_rows=exact_rows,
                        min_rows=min_rows,
                        max_rows=max_rows,
                    )

                generation_plan = DataframeGenerator.create(
                    num_columns=num_columns,
                    exact_rows=exact_rows,
                )
                missingness_plan = DataframeMissingnessModifier.create(
                    num_columns=num_columns,
                )

            elif generation_plan is None:
                if row_plan is None:
                    row_plan = RowCountWidget(
                        exact_rows=exact_rows,
                        min_rows=min_rows,
                        max_rows=max_rows,
                    )

                generation_plan = DataframeGenerator.create(
                    num_columns=missingness_plan.num_columns,
                    exact_rows=exact_rows,
                )

            elif missingness_plan is None:
                missingness_plan = DataframeMissingnessModifier.create(
                    num_columns=generation_plan.num_columns,
                )

                row_plan = generation_plan.row_plan

            else:
                assert generation_plan.num_columns == missingness_plan.num_columns

            column_generators = []
            for i in range(generation_plan.num_columns):
                column_generator = cls._generate_column_generator(
                    generation_plan.column_generators[i],
                    missingness_plan.column_modifiers[i],
                )
                column_generators.append(column_generator)

        else:
            if row_plan is None:
                row_plan = RowCountWidget(
                    exact_rows=exact_rows,
                    min_rows=min_rows,
                    max_rows=max_rows,
                )

        return cls(
            column_generators=column_generators,
            row_plan=row_plan,
        )
    
    def generate(
        self,
        add_missingness: bool = True,
    ) -> pd.DataFrame:
        """
        Generate a dataframe with the specified number of rows and columns, with missingness applied
        
        Parameters:
            add_missingness: Whether to add missingness to the generated dataframe
        """

        series_dict = {}
        for i, column_generator in enumerate(self.column_generators):
            new_series = column_generator.generate(
                n=self.num_rows,
            )

            if add_missingness:
                column_modifier = column_generator

                missified_series = column_modifier.modify(
                    new_series,
                )
            else:
                missified_series = new_series

            series_dict[column_generator.name] = missified_series

        df = pd.DataFrame(series_dict)

        return df

    @staticmethod
    def _generate_column_generator(
        column_generation_plan: ColumnGenerator,
        column_missingness_plan: ColumnMissingnessModifier,
    ) -> ColumnMissingnessModifier:
        missingness_type = column_missingness_plan.missingness_type

        if missingness_type == "ALWAYS":
            return MissingFakerColumnGenerator(
                name=column_generation_plan.name,
                missingness_type=missingness_type,
                faker_type=column_generation_plan.faker_type,
            )

        elif missingness_type == "NEVER":
            return MissingFakerColumnGenerator(
                name=column_generation_plan.name,
                missingness_type=missingness_type,
                faker_type=column_generation_plan.faker_type,
            )

        elif missingness_type == "PROPORTIONAL":
            return MissingFakerColumnGenerator(
                name=column_generation_plan.name,
                missingness_type=missingness_type,
                faker_type=column_generation_plan.faker_type,
                missingness_params=ProportionalColumnMissingnessParams(
                    proportion=column_missingness_plan.missingness_params.proportion,
                ),
            )
