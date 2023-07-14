A python package to create synthetic datasets with realistic patterns of missingness.

It covers the following cases:

	* Columns that are never missing
	* Columns that are always missing
	* Columns that are missing some fraction of the time
	* Columns where the probability of missingness is contingent on the value of another other column

It includes tests for each of these methods.

The top-level API look like this:

```
generate_missing_data(
	n_rows : int = 200, #the number of rows to generate,
	n_cols : int = 10,  #the number of columns to generate,
  missingness_type_list Optional[Dict[string, missingness_pattern]] = None #a dictionary of column names and patterns of missingness to use to populate. If this is ommitted, columns and missingness categories will be created at random
)
```

