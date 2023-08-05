import missingness_data_generator as mdg

def test__generate_dataframe_with_missingness():
    df = mdg.generate_series()
    print(df)