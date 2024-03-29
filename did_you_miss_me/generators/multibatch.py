from abc import ABC
import random
from pydantic import Field
from typing import List, Optional

import pandas as pd

from did_you_miss_me.abc import (
    DataGenerator,
)
from did_you_miss_me.generators.dataframe import (
    DataframeGenerator,
    MissingFakerDataframeGenerator,
)
from did_you_miss_me.generators.row_count_widget import (
    RowCountWidget,
)
from did_you_miss_me.generators.timestamps_and_ids import (
    Indexes,
)


class EpochGenerator(DataGenerator, ABC):
    """
    Abstract base class for EpochGenerators
    """

    pass


class MissingFakerEpochGenerator(EpochGenerator):
    missing_faker_dataframe_generator: MissingFakerDataframeGenerator = Field(
        default_factory=MissingFakerDataframeGenerator.create,
        description="Generator the dataframes in this epoch.",
    )
    num_batches: int = Field(
        default_factory=lambda: int(random.uniform(0, 10) ** 2),
        description="The number of batches to generate in this epoch.",
    )

    @classmethod
    def create(
        cls,
        dataframe_generator: Optional[DataframeGenerator] = None,
        num_batches: Optional[int] = None,
        add_missingness: bool = True,
        # next_indexes: Optional[Indexes] = None,
    ) -> "MissingFakerEpochGenerator":
        """Create a plan for generating an Epoch, with missingness and Faker data.

        Args:
            dataframe_generator (DataframeGenerator): A basic (no missingness) generator for this epoch.
            num_batches (int): The number of batches to generate in this epoch.

        Note:
            `dataframe_generator` will be used to create a MissingFakerDataframeGenerator.
        """
        if num_batches is None:
            num_batches = int(random.uniform(0, 10) ** 2)

        if dataframe_generator is None:
            dataframe_generator = DataframeGenerator.create()

        missing_faker_dataframe_generator = MissingFakerDataframeGenerator.create_using_dataframe_generator(
            dataframe_generator=dataframe_generator,
            add_missingness=add_missingness,
        )

        return cls(
            missing_faker_dataframe_generator=missing_faker_dataframe_generator,
            num_batches=num_batches,
        )


class MultiBatchGenerator(DataGenerator, ABC):
    """
    Abstract base class for MultiBatchGenerators
    """

    pass


class MissingFakerMultiBatchGenerator(MultiBatchGenerator):
    epochs: List[MissingFakerEpochGenerator]

    @property
    def num_epochs(self):
        return len(self.epochs)

    @classmethod
    def create(
        cls,
        epochs: Optional[List[MissingFakerEpochGenerator]] = None,
        exact_rows: Optional[int] = None,
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None,
        num_columns: Optional[int] = None,
        num_epochs: Optional[int] = None,
        batches_per_epoch: Optional[int] = None,
        include_batch_id=False,
        include_primary_key=False,
        include_foreign_keys=False,
        include_timestamps: bool = False,
        add_missingness: bool = True,
    ):
        if epochs is None:
            if num_epochs is None:
                num_epochs = random.randint(3, 6)

            # By default, all epochs share the same generator; only the missingness modifiers vary.
            # As a result, we need a generator, which will be shared across all epochs.
            dataframe_generator = DataframeGenerator.create(
                exact_rows=exact_rows,
                min_rows=min_rows,
                max_rows=max_rows,
                num_columns=num_columns,
                include_batch_id=include_batch_id,
                include_primary_key=include_primary_key,
                include_foreign_keys=include_foreign_keys,
                include_timestamps=include_timestamps,
            )

            epochs = [
                MissingFakerEpochGenerator.create(
                    dataframe_generator=dataframe_generator,
                    num_batches=batches_per_epoch,
                    add_missingness=add_missingness,
                )
                for _ in range(num_epochs)
            ]

        return cls(
            epochs=epochs,
        )

    def generate(
        self,
        print_updates: bool = False,
        print_mod: int = 5,
        next_indexes: Optional[Indexes] = None,
    ) -> pd.DataFrame:
        multibatch_df = pd.DataFrame()

        if next_indexes is None:
            next_indexes = Indexes.create()

        for j, epoch_generator in enumerate(self.epochs):
            if print_updates:
                print(f"===== Epoch: {j} of {self.num_epochs} =====")

            for k in range(epoch_generator.num_batches):
                if print_updates and k % print_mod == 0:
                    print(f"Batch: {k} of {epoch_generator.num_batches}")

                result_object = epoch_generator.missing_faker_dataframe_generator.generate(
                    next_indexes=next_indexes,
                )

                multibatch_df = pd.concat([multibatch_df, result_object.dataframe], ignore_index=True)
                
                next_indexes = result_object.next_indexes

        return multibatch_df
