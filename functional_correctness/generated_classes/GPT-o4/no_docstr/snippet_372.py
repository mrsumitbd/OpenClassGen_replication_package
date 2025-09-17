class DatasetAddVariable:

    def setup(self, existing_elements):
        self.size = existing_elements
        data = np.arange(self.size)
        self.ds = xr.Dataset({f'var{i}': ('x', data) for i in range(self.size)})

    def time_variable_insertion(self, existing_elements):
        data = np.arange(self.size)
        ds = self.ds.copy()
        for i in range(existing_elements):
            ds[f'new_var_{i}'] = ('x', data)

    def time_merge_two_datasets(self, existing_elements):
        data = np.arange(existing_elements)
        ds2 = xr.Dataset({f'other{i}': ('x', data) for i in range(existing_elements)})
        self.ds.merge(ds2)