import random
from pydantic import BaseModel
from typing import List, Optional

from did_you_miss_me.faker_types import (
    FAKER_TYPES,
)
from did_you_miss_me.plans.abc import (
    DataGenerator,
    MissingnessPlan,
)
from did_you_miss_me.plans.column_level import (
    ColumnGenerator,
    FakerColumnGenerator,
    MissingFakerColumnGenerator,
    ColumnMissingnessType,
    ColumnMissingnessPlan,
    ProportionalColumnMissingnessParams,
)


class DataframeRowGenerationPlan(BaseModel):
    num_rows: Optional[int]
    min_rows: Optional[int]
    max_rows: Optional[int]

    @property
    def num_rows(self):
        if self._num_rows is not None:
            return self._num_rows
        else:
            return random.randint(self._min_rows, self._max_rows)

    def __init__(
        self,
        num_rows: Optional[int] = None,
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None,
    ):
        has_min_max = (min_rows is not None) and (max_rows is not None)

        if min_rows is None and max_rows is not None:
            raise ValueError("If you specify max_rows, you must also specify min_rows.")

        elif min_rows is not None and max_rows is None:
            raise ValueError("If you specify min_rows, you must also specify max_rows.")

        if num_rows is None and not has_min_max:
            if random.random() < 0.5:
                num_rows = random.randint(100, 500)
            else:
                min_rows = random.randint(50, 400)
                max_rows = random.randint(min_rows, min_rows + 100)

        elif num_rows is not None and has_min_max:
            raise ValueError("You cannot specify both num_rows and min_rows/max_rows.")

        super().__init__(
            num_rows=num_rows,
            min_rows=min_rows,
            max_rows=max_rows,
        )


class DataframeGenerator(DataGenerator):
    column_generators: List[ColumnGenerator]
    row_plan: DataframeRowGenerationPlan

    @property
    def num_columns(self):
        return len(self.column_generators)

    @property
    def num_rows(self):
        return self.row_plan.num_rows

    def __init__(
        self,
        column_generators: Optional[List[ColumnGenerator]] = None,
        row_plan: Optional[DataframeRowGenerationPlan] = None,
        num_rows: Optional[int] = None,
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
            row_plan = DataframeRowGenerationPlan(
                num_rows=num_rows,
                min_rows=min_rows,
                max_rows=max_rows,
            )

        super().__init__(
            column_generators=column_generators,
            row_plan=row_plan,
        )


class DataframeMissingnessPlan(MissingnessPlan):
    column_generators: List[ColumnMissingnessPlan]

    @property
    def num_columns(self):
        return len(self.column_generators)

    def __init__(
        self,
        column_generators: Optional[List[ColumnMissingnessPlan]] = None,
        num_columns: Optional[int] = None,
    ):
        if column_generators is None:
            if num_columns is None:
                num_columns = 12

            column_generators = []
            for i in range(num_columns):
                column_generator = self._generate_column_generator()
                column_generators.append(column_generator)

        super().__init__(
            column_generators=column_generators,
        )

    @staticmethod
    def _generate_column_generator(
        missingness_type: Optional[ColumnMissingnessType] = None,
    ) -> ColumnMissingnessPlan:
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
            return ColumnMissingnessPlan(
                missingness_type=missingness_type,
            )

        elif missingness_type == ColumnMissingnessType.NEVER:
            return ColumnMissingnessPlan(
                missingness_type=missingness_type,
            )

        elif missingness_type == ColumnMissingnessType.PROPORTIONAL:
            # A little math to make most proportions close to 0 or 1, with "close to 0" being more likely
            proportion = random.random() ** 3
            if random.random() < 0.25:
                proportion = 1 - proportion

            return ColumnMissingnessPlan(
                missingness_type=missingness_type,
                missingness_params=ProportionalColumnMissingnessParams(
                    proportion=proportion,
                ),
            )


class MissingFakerDataframeGenerator(DataGenerator):
    column_generators: List[ColumnGenerator]
    row_plan: DataframeRowGenerationPlan

    @property
    def num_rows(self):
        return self.row_plan.num_rows

    def __init__(
        self,
        column_generators: Optional[List[ColumnGenerator]] = None,
        row_plan: Optional[DataframeRowGenerationPlan] = None,
        generation_plan: Optional[DataframeGenerator] = None,
        missingness_plan: Optional[DataframeMissingnessPlan] = None,
        num_columns: Optional[int] = None,
        num_rows: Optional[int] = None,
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None,
    ):
        if column_generators is None:
            if generation_plan is None and missingness_plan is None:
                if num_columns is None:
                    num_columns = 12

                if row_plan is None:
                    row_plan = DataframeRowGenerationPlan(
                        num_rows=num_rows,
                        min_rows=min_rows,
                        max_rows=max_rows,
                    )

                generation_plan = DataframeGenerator(
                    num_columns=num_columns,
                    num_rows=num_rows,
                )
                missingness_plan = DataframeMissingnessPlan(
                    num_columns=num_columns,
                )

            elif generation_plan is None:
                if row_plan is None:
                    row_plan = DataframeRowGenerationPlan(
                        num_rows=num_rows,
                        min_rows=min_rows,
                        max_rows=max_rows,
                    )

                generation_plan = DataframeGenerator(
                    num_columns=missingness_plan.num_columns,
                    num_rows=num_rows,
                )

            elif missingness_plan is None:
                missingness_plan = DataframeMissingnessPlan(
                    num_columns=generation_plan.num_columns,
                )

                row_plan = generation_plan.row_plan

            else:
                assert generation_plan.num_columns == missingness_plan.num_columns

            column_generators = []
            for i in range(generation_plan.num_columns):
                column_generator = self._generate_column_generator(
                    generation_plan.column_generators[i],
                    missingness_plan.column_generators[i],
                )
                column_generators.append(column_generator)

        else:
            if row_plan is None:
                row_plan = DataframeRowGenerationPlan(
                    num_rows=num_rows,
                    min_rows=min_rows,
                    max_rows=max_rows,
                )

        super().__init__(
            column_generators=column_generators,
            row_plan=row_plan,
        )

    @staticmethod
    def _generate_column_generator(
        column_generation_plan: ColumnGenerator,
        column_missingness_plan: ColumnMissingnessPlan,
    ) -> ColumnMissingnessPlan:
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