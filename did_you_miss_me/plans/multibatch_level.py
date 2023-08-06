import random
from typing import List, Optional

from did_you_miss_me.plans.abc import (
    DataGenerator,
)
from did_you_miss_me.plans.dataframe_level import (
    DataframeGenerator,
    MissingFakerDataframeGenerator,
)


class EpochGenerator(DataGenerator):
    dataframe_plan: MissingFakerDataframeGenerator
    num_batches: int

    def __init__(
        self,
        dataframe_plan: Optional[MissingFakerDataframeGenerator] = None,
        generation_plan: Optional[DataframeGenerator] = None,
        num_batches: Optional[int] = None,
    ):
        if num_batches is None:
            num_batches = int(random.uniform(0, 10) ** 2)

        if dataframe_plan is None:
            if generation_plan is None:
                generation_plan = DataframeGenerator.create()

            dataframe_plan = MissingFakerDataframeGenerator.create(
                generation_plan=generation_plan,
            )

        super().__init__(
            dataframe_plan=dataframe_plan,
            num_batches=num_batches,
        )


class MultiBatchGenerator(DataGenerator):
    epochs: List[EpochGenerator]

    @property
    def num_epochs(self):
        return len(self.epochs)

    def __init__(
        self,
        epochs: Optional[List[EpochGenerator]] = None,
        exact_rows: Optional[int] = None,
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None,
        num_columns: Optional[int] = None,
        num_epochs: Optional[int] = None,
        batches_per_epoch: Optional[int] = None,
    ):
        if epochs is None:
            if num_epochs is None:
                num_epochs = random.randint(3, 6)

            # By default, all epochs have the same generation plan; only the missingness plans vary.
            # As a result, we need a generation plan, which will be shared across all epochs.
            generation_plan = DataframeGenerator.create(
                exact_rows=exact_rows,
                min_rows=min_rows,
                max_rows=max_rows,
                num_columns=num_columns,
            )

            epochs = [
                EpochGenerator(
                    generation_plan=generation_plan,
                    num_batches=batches_per_epoch,
                )
                for _ in range(num_epochs)
            ]

        super().__init__(
            epochs=epochs,
        )
