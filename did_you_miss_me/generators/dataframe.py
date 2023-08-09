import random
from typing import List, Optional

import pandas as pd

from did_you_miss_me.faker_types import (
    FAKER_TYPES,
)
from did_you_miss_me.abc import (
    DataGenerator,
)
from did_you_miss_me.generators.column import (
    ColumnGenerator,
    FakerColumnGenerator,
    MissingFakerColumnGenerator,
)
from did_you_miss_me.generators.row_count_widget import (
    RowCountWidget,
)
from did_you_miss_me.generators.timestamps_and_ids import (
    TimeStampAndIdMultiColumnGenerator,
)
from did_you_miss_me.modifiers.missingness import (
    ColumnMissingnessType,
    ColumnMissingnessModifier,
    ProportionalColumnMissingnessParams,
    DataframeMissingnessModifier,
)


class DataframeGenerator(DataGenerator):
    column_generators: List[ColumnGenerator]
    row_count_widget: RowCountWidget
    timestamp_and_id_generator: Optional[TimeStampAndIdMultiColumnGenerator]

    @property
    def num_columns(self):
        return len(self.column_generators)

    @property
    def num_rows(self):
        return self.row_count_widget.num_rows

    @classmethod
    def create(
        cls,
        num_columns: Optional[int] = None,
        exact_rows: Optional[int] = None,
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None,
        include_ids: bool = False,
        include_timestamps: bool = False,
    ):
        if num_columns is None:
            num_columns = 12

        column_generators = []
        for i in range(num_columns):
            column_generator = FakerColumnGenerator(
                name=f"column_{i + 1}",
                faker_type=random.choice(FAKER_TYPES),
            )
            column_generators.append(column_generator)

        row_count_widget = RowCountWidget.create(
            exact_rows=exact_rows,
            min_rows=min_rows,
            max_rows=max_rows,
        )

        if (include_ids is not None) or (include_timestamps is not None):
            timestamp_and_id_generator = TimeStampAndIdMultiColumnGenerator.create(
                include_ids=include_ids,
                include_timestamps=include_timestamps,
            )
        else:
            timestamp_and_id_generator = None

        return cls(
            column_generators=column_generators,
            row_count_widget=row_count_widget,
            timestamp_and_id_generator=timestamp_and_id_generator,
        )


class MissingFakerDataframeGenerator(DataGenerator):
    column_generators: List[MissingFakerColumnGenerator]
    row_count_widget: RowCountWidget
    timestamp_and_id_generator: Optional[TimeStampAndIdMultiColumnGenerator]

    @property
    def num_rows(self):
        return self.row_count_widget.num_rows

    @classmethod
    def create(
        cls,
        row_count_widget: Optional[RowCountWidget] = None,
        timestamp_and_id_generator: Optional[TimeStampAndIdMultiColumnGenerator] = None,

        dataframe_generator: Optional[DataframeGenerator] = None,

        num_columns: Optional[int] = None,
        exact_rows: Optional[int] = None,
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None,
        include_ids: bool = False,
        include_timestamps: bool = False,
        add_missingness: bool = True,
    ):
        if dataframe_generator is None:
            if num_columns is None:
                num_columns = 12

            if row_count_widget is None:
                row_count_widget = RowCountWidget.create(
                    exact_rows=exact_rows,
                    min_rows=min_rows,
                    max_rows=max_rows,
                )

            if timestamp_and_id_generator is None:
                timestamp_and_id_generator = (
                    TimeStampAndIdMultiColumnGenerator.create(
                        include_ids=include_ids,
                        include_timestamps=include_timestamps,
                    )
                )

            dataframe_generator = DataframeGenerator.create(
                num_columns=num_columns,
                exact_rows=exact_rows,
            )

        else:
            num_columns = dataframe_generator.num_columns

            row_count_widget = dataframe_generator.row_count_widget
            timestamp_and_id_generator = (
                dataframe_generator.timestamp_and_id_generator
            )

        if add_missingness:
            missingness_modifier = DataframeMissingnessModifier.create(
                num_columns=num_columns,
            )
        else:
            missingness_modifier = DataframeMissingnessModifier.create(
                num_columns=num_columns,
                missingness_type=ColumnMissingnessType.NEVER,
            )

        column_generators = []
        for i in range(dataframe_generator.num_columns):
            column_generator = cls._generate_column_generator(
                dataframe_generator.column_generators[i],
                missingness_modifier.column_modifiers[i],
            )
            column_generators.append(column_generator)

        return cls(
            column_generators=column_generators,
            row_count_widget=row_count_widget,
            timestamp_and_id_generator=timestamp_and_id_generator,
        )

    def generate(self) -> pd.DataFrame:
        """
        Generate a dataframe with the specified number of rows and columns, with missingness applied
        """

        series_dict = {}
        if self.timestamp_and_id_generator is not None:
            timestamp_and_id_series_dict = self.timestamp_and_id_generator.generate(
                num_rows=self.num_rows,
            )

            series_dict = {**series_dict, **timestamp_and_id_series_dict}

        for i, column_generator in enumerate(self.column_generators):
            new_series = column_generator.generate(
                num_rows=self.num_rows,
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

        if missingness_type in ["ALWAYS", "NEVER"]:
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
