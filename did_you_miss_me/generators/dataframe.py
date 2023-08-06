import random
from typing import List, Optional

import pandas as pd

from did_you_miss_me.faker_types import (
    FAKER_TYPES,
)
from did_you_miss_me.abc import (
    DataGenerator,
    # MissingnessModifier,
)

# from did_you_miss_me.plans.column_level import (
#     ColumnGenerator,
#     FakerColumnGenerator,
#     MissingFakerColumnGenerator,
#     ColumnMissingnessType,
#     ColumnMissingnessModifier,
#     ProportionalColumnMissingnessParams,
# )
from did_you_miss_me.generators.row_count_widget import (
    RowCountWidget,
)
from did_you_miss_me.generators.column import (
    ColumnGenerator,
    FakerColumnGenerator,
    MissingFakerColumnGenerator,
)
from did_you_miss_me.modifiers.missingness import (
    ColumnMissingnessModifier,
    ProportionalColumnMissingnessParams,
    DataframeMissingnessModifier,
)


class DataframeGenerator(DataGenerator):
    column_generators: List[ColumnGenerator]
    row_count_widget: RowCountWidget

    @property
    def num_columns(self):
        return len(self.column_generators)

    @property
    def num_rows(self):
        return self.row_count_widget.num_rows

    @classmethod
    def create(
        cls,
        column_generators: Optional[List[ColumnGenerator]] = None,
        num_columns: Optional[int] = None,
        row_count_widget: Optional[RowCountWidget] = None,
        exact_rows: Optional[int] = None,
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None,
    ):
        assert (column_generators is None) or (
            num_columns is None
        ), "You cannot specify both column_generators and num_columns."
        assert (
            (row_count_widget is None)
            or (exact_rows is None)
            or (min_rows is None and max_rows is None)
        ), "You cannot specify row_count_widget, exact_rows, and min_rows/max_rows."

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

        if row_count_widget is None:
            row_count_widget = RowCountWidget(
                exact_rows=exact_rows,
                min_rows=min_rows,
                max_rows=max_rows,
            )

        return cls(
            column_generators=column_generators,
            row_count_widget=row_count_widget,
        )


class MissingFakerDataframeGenerator(DataGenerator):
    column_generators: List[MissingFakerColumnGenerator]
    row_count_widget: RowCountWidget

    @property
    def num_rows(self):
        return self.row_count_widget.num_rows

    @classmethod
    def create(
        cls,
        column_generators: Optional[List[ColumnGenerator]] = None,
        row_count_widget: Optional[RowCountWidget] = None,
        dataframe_generator: Optional[DataframeGenerator] = None,
        missingness_modifier: Optional[DataframeMissingnessModifier] = None,
        num_columns: Optional[int] = None,
        exact_rows: Optional[int] = None,
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None,
    ):
        if column_generators is None:
            if dataframe_generator is None and missingness_modifier is None:
                if num_columns is None:
                    num_columns = 12

                if row_count_widget is None:
                    row_count_widget = RowCountWidget(
                        exact_rows=exact_rows,
                        min_rows=min_rows,
                        max_rows=max_rows,
                    )

                dataframe_generator = DataframeGenerator.create(
                    num_columns=num_columns,
                    exact_rows=exact_rows,
                )
                missingness_modifier = DataframeMissingnessModifier.create(
                    num_columns=num_columns,
                )

            elif dataframe_generator is None:
                if row_count_widget is None:
                    row_count_widget = RowCountWidget(
                        exact_rows=exact_rows,
                        min_rows=min_rows,
                        max_rows=max_rows,
                    )

                dataframe_generator = DataframeGenerator.create(
                    num_columns=missingness_modifier.num_columns,
                    exact_rows=exact_rows,
                )

            elif missingness_modifier is None:
                missingness_modifier = DataframeMissingnessModifier.create(
                    num_columns=dataframe_generator.num_columns,
                )

                row_count_widget = dataframe_generator.row_count_widget

            else:
                assert (
                    dataframe_generator.num_columns == missingness_modifier.num_columns
                )

            column_generators = []
            for i in range(dataframe_generator.num_columns):
                column_generator = cls._generate_column_generator(
                    dataframe_generator.column_generators[i],
                    missingness_modifier.column_modifiers[i],
                )
                column_generators.append(column_generator)

        else:
            if row_count_widget is None:
                row_count_widget = RowCountWidget(
                    exact_rows=exact_rows,
                    min_rows=min_rows,
                    max_rows=max_rows,
                )

        return cls(
            column_generators=column_generators,
            row_count_widget=row_count_widget,
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
                num_rows=self.num_rows,
                add_missingness=add_missingness,
            )

            series_dict[column_generator.name] = new_series

        df = pd.DataFrame(series_dict)

        return df

    @staticmethod
    def _generate_column_generator(
        column_generator: ColumnGenerator,
        column_missingness_modifier: ColumnMissingnessModifier,
    ) -> ColumnMissingnessModifier:
        missingness_type = column_missingness_modifier.missingness_type

        if missingness_type == "ALWAYS":
            return MissingFakerColumnGenerator(
                name=column_generator.name,
                missingness_type=missingness_type,
                faker_type=column_generator.faker_type,
            )

        elif missingness_type == "NEVER":
            return MissingFakerColumnGenerator(
                name=column_generator.name,
                missingness_type=missingness_type,
                faker_type=column_generator.faker_type,
            )

        elif missingness_type == "PROPORTIONAL":
            return MissingFakerColumnGenerator(
                name=column_generator.name,
                missingness_type=missingness_type,
                faker_type=column_generator.faker_type,
                missingness_params=ProportionalColumnMissingnessParams(
                    proportion=column_missingness_modifier.missingness_params.proportion,
                ),
            )
