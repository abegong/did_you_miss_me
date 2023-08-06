# DidYouMissMe

`did_you_miss_me` is a python package to create datasets with realistic patterns of missingness.

I'm also using it as a test case to figure out general patterns for data synthesis tooling.

Key features:

* Generate synthetic datasets with a huge range of variable types and realistic patterns of missingness
* (Use AI/LLMs to create datasets with sensible variable names, types, and values.)
* You can also add missingness to existing datasets.
* Includes logic for generating missingness with MCAR, (MAR), and MNAR statistical properties.
* Basic use cases work in seconds, with a single line of code; no configuration needed.
* For advanced users, the concept of `DataTools` such as `DataGenerators` and `DataModifiers` gives you very granular control over how data is created and missingness is added.
* (Includes utility functions to save data in several formats, such as SQLite, or namespaced folders of .csv, .tsv, or parquet files.)

Stuff in (parentheses) is aspirational---not yet built.

## Quickstart
Use `generate_dataframe` to create synthetic datasets from scratch.

```
import did_you_miss_me as dymm

dymm.generate_dataframe(
    exact_rows=10,
    num_columns=7,
)
```

Returns something like:

|    |   column_1 | column_2        |   column_3 | column_4   | column_5                                         | column_6   | column_7     |
|---:|-----------:|:----------------|-----------:|:-----------|:-------------------------------------------------|:-----------|:-------------|
|  0 |      21610 |                 |    6306090 |            | Age head adult democratic put though kid.        | 06:06:42   |              |
|  1 |      31906 |                 |    2322383 |            | Standard contain force.                          | 19:47:29   |              |
|  2 |      87239 | ['b', 'c', 'a'] |     319679 |            | East reduce PM community situation forward dark. |            |              |
|  3 |      70427 | ['a']           |    8480857 |            | Economic tax budget whom despite number occur.   | 00:19:37   |              |
|  4 |      06080 | ['b', 'a']      |    6779036 |            | May eight fly point character less.              | 06:03:24   |              |
|  5 |      81049 | ['a', 'b', 'c'] |     620417 |            | Dream size subject list team.                    | 13:30:23   | Thompson Inc |
|  6 |      55782 | ['a', 'b', 'c'] |    6387661 |            | Too also argue sit area group political street.  |            |              |
|  7 |      29531 | ['b', 'a', 'c'] |    3383294 |            | Forward education together fall.                 | 07:13:48   |              |
|  8 |      99760 |                 |    3594189 |            | Away animal level question never each.           | 10:38:25   |              |
|  9 |      99606 |                 |    1236934 |            | Themselves similar become front city physical.   |            |              |

By default, datasets are generated using random types from the `Faker` library, and tend to feel pretty random.


<!-- ## Use AI to generate realistic-looking data sets
The `use_ai` and `prompt` parameters let you use LLMs to generate more coherent dataframes.

```
dymm.generate_dataframe(
    exact_rows=10,
    num_columns=7,
    use_ai="OpenAI",
    prompt="blood drives",
)
```

|DonationDriveID|BloodBankID|DriveName               | State | Zipcode | StartDate         |EndDate            |
|---------------|-----------|------------------------|-------|---------|-------------------|-------------------|
|1              |1          |Summer Donations        | CA    |         |2020-06-01 00:00:00|2020-06-30 23:59:59|
|2              |2          |Fall Blood Drive        | UT    |         |2020-09-01 00:00:00|2020-09-30 23:59:59|
|3              |           |Winter Blood Drive      | AK    |         |                   |                   |
|4              |4          |Spring Donations        | VA    |         |2021-03-01 00:00:00|2021-03-31 23:59:59|
|5              |           |Back to School Donations| NY    |         |2020-08-01 00:00:00|2020-08-31 23:59:59|
|6              |2          |Thanksgiving Blood Drive| VA    |         |                   |                   |
|7              |3          |Holiday Blood Drive     | TX    |         |                   |                   |
|8              |           |Spring Blood Drive      | CA    |         |2021-03-15 00:00:00|2021-04-15 23:59:59|
|9              |           |Summer Blood Drive      | AL    |         |                   |                   |
|10             |2          |Fall Donations          | MI    |         |2020-09-15 00:00:00|2020-10-15 23:59:59|

Connections and prompt chaining are managed through `langchain`. To use `did_you_miss_me` in this mode, you'll need to install it with: `pip install did_you_miss_me[ai]` -->

## Missification

The `missify` operation allows you to add missingness to an existing dataframe. For example, here's polling data from fivethirtyeight.

```
import pandas as pd
df = pd.read_csv('https://projects.fivethirtyeight.com/polls/data/favorability_polls.csv')

dymm.missify_dataframe(df)
```
Before:

|    |   poll_id |   pollster_id | pollster         |   sponsor_ids | sponsors   | display_name     |   pollster_rating_id | pollster_rating_name   |...|
|---:|----------:|--------------:|:-----------------|--------------:|:-----------|:-----------------|---------------------:|:-----------------------|---|
|  0 |     83346 |           241 | Ipsos            |           379 | ABC News   | Ipsos            |                  154 | Ipsos                  |...|
|  1 |     83346 |           241 | Ipsos            |           379 | ABC News   | Ipsos            |                  154 | Ipsos                  |...|
|  2 |     83331 |           568 | YouGov           |           352 | Economist  | YouGov           |                  391 | YouGov                 |...|
|  3 |     83331 |           568 | YouGov           |           352 | Economist  | YouGov           |                  391 | YouGov                 |...|
|  4 |     83331 |           568 | YouGov           |           352 | Economist  | YouGov           |                  391 | YouGov                 |...|
|  5 |     83331 |           568 | YouGov           |           352 | Economist  | YouGov           |                  391 | YouGov                 |...|
|  6 |     83331 |           568 | YouGov           |           352 | Economist  | YouGov           |                  391 | YouGov                 |...|
|  7 |     83331 |           568 | YouGov           |           352 | Economist  | YouGov           |                  391 | YouGov                 |...|
|  8 |     83316 |          1302 | Echelon Insights |           nan | nan        | Echelon Insights |                  407 | Echelon Insights       |...|
|  9 |     83316 |          1302 | Echelon Insights |           nan | nan        | Echelon Insights |                  407 | Echelon Insights       |...|

After:

|    |   poll_id |   pollster_id | pollster         | sponsor_ids   | sponsors   | display_name   |   pollster_rating_id | pollster_rating_name   |...|
|---:|----------:|--------------:|:-----------------|:--------------|:-----------|:---------------|---------------------:|:-----------------------|---|
|  0 |     83346 |           nan | Ipsos            |               | ABC News   | Ipsos          |                  nan |                        |...|
|  1 |     83346 |           241 | Ipsos            |               |            |                |                  nan | Ipsos                  |...|
|  2 |     83331 |           568 | YouGov           |               |            |                |                  391 |                        |...|
|  3 |     83331 |           nan | YouGov           |               |            |                |                  nan | YouGov                 |...|
|  4 |     83331 |           568 | YouGov           |               |            |                |                  nan | YouGov                 |...|
|  5 |     83331 |           568 |                  |               | Economist  |                |                  nan | YouGov                 |...|
|  6 |     83331 |           568 | YouGov           |               | Economist  |                |                  nan | YouGov                 |...|
|  7 |     83331 |           568 | YouGov           |               | Economist  |                |                  nan | YouGov                 |...|
|  8 |     83316 |          1302 | Echelon Insights |               | nan        |                |                  nan | Echelon Insights       |...|
|  9 |     83316 |          1302 | Echelon Insights |               | nan        |                |                  nan | Echelon Insights       |...|


## For more info...

Please see the code itself. Most modules and methods have decent docstrings. If something is unclear, please create a github issue.

Pull requests welcome!

TDD-lite: not (yet) fully testing all of the API surface area. Instead, I've been testing classes and methods as I've discovered bugs, refactored them, or described them in documentation.

## Todo
* Create `DataframeMissingnessModifier.modify` and think through syntax + APIs for `DataModifier` classes.
    * api.missify_dataframe -> DataframeMissingnessModifier.modify

* Reorg code to separate Generators and Modifiers
    * Pull RowCountWidget into its own file
    * Pull ColumnMissingnessParams and related code into its own file
* Refactor tests to cover 1. integration tests at the API level, and 2. tests for specific Plans

* Add ability to create SQLlite DBs
* Add ability to save to mutilple files

* Create a CLI on top of the primary API methods

* Create an TimestampsAndIDsWidget
    * Activate include_ids param
    * Activate include_timestamps param

* Add conditional missingness
* Add langchain stuffs
* Publish to pypi