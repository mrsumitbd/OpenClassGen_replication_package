class DatasetAddVariable:

    def setup(self, existing_elements):
        # Create initial dataset with existing elements
        self.df1 = pd.DataFrame({
            'id': range(existing_elements),
            'value1': np.random.randn(existing_elements),
            'category': np.random.choice(['A', 'B', 'C'], existing_elements)
        })
        
        # Create second dataset for merging
        self.df2 = pd.DataFrame({
            'id': range(existing_elements),
            'value2': np.random.randn(existing_elements),
            'group': np.random.choice(['X', 'Y', 'Z'], existing_elements)
        })
        
        # Create a copy for insertion test
        self.df_copy = self.df1.copy()

    def time_variable_insertion(self, existing_elements):
        # Add a new column/variable to the dataset
        self.df_copy['new_variable'] = np.random.randn(existing_elements)

    def time_merge_two_datasets(self, existing_elements):
        # Merge two datasets on the 'id' column
        merged_df = pd.merge(self.df1, self.df2, on='id', how='inner')
        return merged_df