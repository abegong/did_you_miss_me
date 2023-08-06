# Abstractions Overview #

Most of the business logic in `did_you_miss_me` is based on two core concepts: `DataGenerators` and `DataModifiers`. Both are based on an abstract base class called `DataTool`.

* `DataGenerators` are used to generate data from scratch.
* `DataModifiers` are used to modify existing data.

These two classes work together to create a wide variety of data generation and modification patterns. One common pattern is for generators to wrap modifiers. The generator creates data, and then modifies that data before returning it. This allows quite complicated data generators to be created from relatively simple building blocks.

## Data objects ##

`DataGenerators` and `DataModifiers` can be applied to several kinds of data objects:

* A `Column` is a 1-dimensional array of data, like a column in a table or spreadsheet. Columns can also include lists and vectors. `did_you_miss_me` uses the `pandas.Series` for most column-level operations.
* A `DataFrame` is a 2-dimensional array of data, like a table or spreadsheet. `did_you_miss_me` uses the `pandas.DataFrame` for most  `DataFrame` operations.
* An `Epoch` is a list of DataFrames that share the same data-generating process.
* A `Multibatch` is a list of Epochs. Because each Epoch can have a different data-generating process, a Multibatch can be used to simulate a dataset where data changes and evolves over time.



## Indirect instantiation via .create and .create_* methods ##

All generators and modifiers support a `.create()` method, which will instantiate a generator or modifier based on sensible defaults. Random values are often used, so running `.create` repeatedly will usually create a wide variety of different generators or modifiers.

    my_generator = MyDataGenerator.create()
    my_modifier = MyDataModifier.create()

The `create` method might include some arguments, but those arguments are always optional. Therefore, you can always create a generator or modifier by calling `.create()` with no arguments.

In most cases, `create` accepts a variety of optional convenience arguments, which are used to create the generator or modifier. These arguments are not usually the same as the arguments to the generator or modifier's constructor.

    {{Examples}}
    my_generator = SomeDataGenerator.create(
        ...params...
    )
    my_modifier = SomeDataModifier.create(
        ...params...
    )

Some generators and modifiers support additional `.create_from_*` or `.create_by_*` methods. This is done when there are multiple ways you might want to create a generator or modifier, and cramming all of them into a single `.create()` method would be too confusing.

    SomeDataGenerator.create_from_*(
        ...params...
    )

    SomeDataGenerator.create_from_*(
        ...params...
    )

## Direct instantiation via constructor ##
    
If you know exactly how a given generator or modifier works, you can always instantiate DataGenerators and DataModifiers directly.

    my_generator = MyDataGenerator(...params...)
    my_modifier = MyDataModifier(...params...)


usually instantiated with a dictionary of parameters. This is because they are often created from JSON files, and JSON files are usually dictionaries.

## Execution ##
    new_data = my_generator.generate()
    new_data = my_modifier.modify(some_data)

    MyDataModifier.modify(some_data)

    ## Reproducibility ##
    * Given an appropriate random seed

    Plans are designed to be immutable. Once you create a Plan, you cannot change it.


## Serialization ##
    DataManipulators are subclassed from pydantic's BaseModel, so you can use convenience methods like `.dict()` and `.json()` to inspect them.

    Plans are designed to be serializable. You can convert a Plan to a dictionary using the .to_dict() method, and you can convert a dictionary to a Plan using the .from_dict() method.


    Abstract class for plans.

    There are two types of plans: generator plans and missingness plans.
    Generator plans are used to generate data, and missingness plans are used to
    add missingness ("missify") data.

    

