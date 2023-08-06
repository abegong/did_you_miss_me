import random
from pydantic import Field
from typing import List, Optional

import pandas as pd

from did_you_miss_me.plans.abc import (
    DataGenerator,
)
from did_you_miss_me.plans.dataframe_level import (
    DataframeGenerator,
    MissingFakerDataframeGenerator,
)

class EpochGenerator(DataGenerator):
    dataframe_plan: MissingFakerDataframeGenerator = Field(
        default_factory=MissingFakerDataframeGenerator.create,
        description="The plan for generating the dataframes in this epoch.",
    )
    num_batches: int = Field(
        default_factory=lambda: int(random.uniform(0, 10) ** 2),
        description="The number of batches to generate in this epoch.",
    )

    @classmethod
    def create(
        cls,
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

        return cls(
            dataframe_plan=dataframe_plan,
            num_batches=num_batches,
        )


class MultiBatchGenerator(DataGenerator):
    epochs: List[EpochGenerator]

    @property
    def num_epochs(self):
        return len(self.epochs)

    @classmethod
    def create(
        cls,
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
                EpochGenerator.create(
                    generation_plan=generation_plan,
                    num_batches=batches_per_epoch,
                )
                for _ in range(num_epochs)
            ]

        return cls(
            epochs=epochs,
        )
    
    def generate(
        self,
        add_missingness: bool = True,
    ) -> pd.DataFrame:
        multibatch_df = pd.DataFrame()

        batch_id = 0
        for j, epoch_plan in enumerate(self.epochs):
            # print(f"Epoch: {j} of {multibatch_plan.num_epochs}")

            for k in range(epoch_plan.num_batches):
                # print(f"Batch: {k} of {epoch_plan.num_batches}")

                series_dict = {}
                batch_id_series = pd.Series([batch_id] * epoch_plan.dataframe_plan.num_rows)
                series_dict["batch_id"] = batch_id_series

                for i, column_generator in enumerate(
                    epoch_plan.dataframe_plan.column_generators
                ):
                    new_series = column_generator.generate(
                        n=epoch_plan.dataframe_plan.num_rows,
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
                multibatch_df = pd.concat([multibatch_df, df], ignore_index=True)

                batch_id += 1

        return multibatch_df