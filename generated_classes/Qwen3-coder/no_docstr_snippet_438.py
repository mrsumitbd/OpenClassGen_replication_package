class IOWriteNetCDFDask:
    def setup(self):
        # Create sample data with dask arrays
        self.temp_dir = TemporaryDirectory()
        self.file_path = os.path.join(self.temp_dir.name, "test_data.nc")
        
        # Create large dataset with dask arrays
        data_shape = (1000, 1000)
        chunks = (100, 100)
        
        # Create dask arrays
        temp_data = da.random.random(data_shape, chunks=chunks)
        pressure_data = da.random.random(data_shape, chunks=chunks)
        
        # Create xarray dataset
        self.dataset = xr.Dataset(
            {
                'temperature': (['x', 'y'], temp_data),
                'pressure': (['x', 'y'], pressure_data)
            },
            coords={
                'x': np.arange(data_shape[0]),
                'y': np.arange(data_shape[1])
            }
        )

    def time_write(self):
        # Write the dataset to NetCDF file
        self.dataset.to_netcdf(self.file_path)
        
    def teardown(self):
        # Clean up temporary directory
        self.temp_dir.cleanup()