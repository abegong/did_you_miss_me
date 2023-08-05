A python package to create synthetic datasets with realistic patterns of missingness.

## Basic usage

`missing_data_generator` can generate data with various patterns of missingness.

It can generate a column's worth of data at a time:
```
import missing_data_generator as mdg

mdg.generate_series(
	n = 50,
	faker_type = "email_address",
	mmissingness_type = 
	proportion_missing = 20
)
```
```
> Example Series
```


`missing_data_generator` can generate whole dataframes. By default, it will generate dataframes with several columns of various types.
```
mdg.generate_dataframe()
```
```
> Example dataframe
```



If you install the optional openAI dependency and have your credentials set up, you can call:
```
mdg.generate_dataframe(use_openai=True)
```

This will use AI to generate a more realistic-ish dataframe.
```
> Example dataframe
```



#####


You can override many of the defaults from the `generate_dataframe` method. (If you need finer-grained control, please see the Advanced Usage section.)
```
> Example dataframe
```




You can override many of the defaults from the `generate_dataframe` method. (If you need finer-grained control, please see the Advanced Usage section.)
```
mdg.add_missing_data_to_dataframe()
```
```
> Example dataframe
```



It can also generate dataframes where patterns in missingness change over time. Using the same naming convention as Great Expectations, we call these multibach dataframes.
```
mdg.generate_multibatch_dataframe(
	batches
	epochs
	rows_per_batch
)
```
```
> Example multibatchdataframe
```

All of these methods are available from a CLI:

```
python -m missing_data_generator
```


```
mdg.save_to_sql
```

Each of these method

## Advanced usage
```
import missing_data_generator as mdg

my_dataframe_plan = mdg.plans.DataframePlan(
	columns = [
		mdg.plans.ColumnPlan(
			name="never_missing_column"
			faker_type
		),
		mdg.plans.ColumnPlan(

		),
		mdg.plans.ProportionallyMissingColumnPlan(

		),
		mdg.plans.ConditionallyMissingColumnPlan(
			conditional_column_name : str
			proportions : Dict
		),
	]
)

mdg.generate_dataframe()
```


It covers the following cases:

	* Columns that are never missing
	* Columns that are always missing
	* Columns that are missing some fraction of the time
	* Columns where the probability of missingness is contingent on the value of another other column


MAR, MCAR, MNAR

It includes tests for each of these methods.

The top-level API look like this:

```
generate_missing_data(
	n_rows : int = 200, #the number of rows to generate,
	n_cols : int = 10,  #the number of columns to generate,
	missingness_type_list Optional[Dict[string, missingness_pattern]] = None #a dictionary of column names and patterns of missingness to use to populate. If this is ommitted, columns and missingness categories will be created at random
)


mdg.generate_dataframe
mdg.generate_series

mdg.generate_multibatch_dataframe
mdg.generate_sqlite_database
```

To do:
* Create repo on github
* Add gitignore
* Add setup.py and other scaffolding to create this as a package
* Publish to pypi
* Figure out and document top-level API
* Add documentation to Plans
* Flesh out tests
* Add multibatch planners
* Add ability to create SQLlite DBs
* Add ability to add missingness to an existing dataset
* Add conditional missingness