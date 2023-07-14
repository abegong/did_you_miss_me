class NeverMissingPattern:
    def __init__(self):
        pass
    
    def determine_missingness(self, column_value):
        return False


class AlwaysMissingPattern:
    def __init__(self):
        pass
    
    def determine_missingness(self, column_value):
        return True


class FractionMissingPattern:
    def __init__(self, fraction):
        self.fraction = fraction
    
    def determine_missingness(self, column_value):
        return random.random() < self.fraction


class ContingentMissingPattern:
    def __init__(self, contingency_column, contingency_value, missingness_pattern):
        self.contingency_column = contingency_column
        self.contingency_value = contingency_value
        self.missingness_pattern = missingness_pattern
    
    def determine_missingness(self, column_value, dataset):
        contingency_column_index = dataset.columns.index(self.contingency_column)
        contingency_column_values = dataset[:, contingency_column_index]
        contingency_value_indices = np.where(contingency_column_values == self.contingency_value)[0]
        is_contingency_value = np.isin(np.arange(len(dataset)), contingency_value_indices)
        
        return self.missingness_pattern.determine_missingness(column_value) if is_contingency_value else False