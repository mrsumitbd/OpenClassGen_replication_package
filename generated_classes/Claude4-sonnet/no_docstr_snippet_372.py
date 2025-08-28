class DatasetAddVariable:
    def setup(self, existing_elements):
        self.ds = xr.Dataset()
        for i in range(existing_elements):
            self.ds[f'var_{i}'] = xr.DataArray(
                np.random.randn(100, 50),
                dims=['x', 'y'],
                coords={'x': np.arange(100), 'y': np.arange(50)}
            )
        
        self.new_var = xr.DataArray(
            np.random.randn(100, 50),
            dims=['x', 'y'],
            coords={'x': np.arange(100), 'y': np.arange(50)}
        )
        
        self.ds2 = xr.Dataset({
            'new_var': self.new_var
        })

    def time_variable_insertion(self, existing_elements):
        self.ds['new_variable'] = self.new_var

    def time_merge_two_datasets(self, existing_elements):
        xr.merge([self.ds, self.ds2])