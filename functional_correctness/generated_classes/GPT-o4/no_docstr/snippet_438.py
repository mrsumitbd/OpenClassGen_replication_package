class IOWriteNetCDFDask:

    def setup(self):
        # create a temporary file for writing
        tmp = tempfile.NamedTemporaryFile(suffix='.nc', delete=False)
        self.filename = tmp.name
        tmp.close()

        # create a Dask-backed xarray Dataset
        shape = (2000, 2000)
        chunks = (500, 500)
        data = da.random.random(shape, chunks=chunks)
        self.ds = xr.Dataset(
            {"data": (("x", "y"), data)},
            coords={"x": np.arange(shape[0]), "y": np.arange(shape[1])},
        )

    def time_write(self):
        # write the Dataset to NetCDF
        self.ds.to_netcdf(self.filename, mode="w", engine="netcdf4")