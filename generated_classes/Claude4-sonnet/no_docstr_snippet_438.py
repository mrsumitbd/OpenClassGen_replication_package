class IOWriteNetCDFDask:
    def __init__(self):
        self.ds = None
        self.filename = None

    def setup(self):
        # Create a temporary file
        self.filename = tempfile.mktemp(suffix='.nc')
        
        # Create sample data with dask arrays
        time = np.arange(100)
        lat = np.linspace(-90, 90, 180)
        lon = np.linspace(-180, 180, 360)
        
        # Create dask arrays for the data variables
        temp_data = da.random.random((100, 180, 360), chunks=(10, 60, 120))
        precip_data = da.random.random((100, 180, 360), chunks=(10, 60, 120))
        
        # Create xarray dataset with dask arrays
        self.ds = xr.Dataset({
            'temperature': (['time', 'lat', 'lon'], temp_data),
            'precipitation': (['time', 'lat', 'lon'], precip_data)
        }, coords={
            'time': time,
            'lat': lat,
            'lon': lon
        })

    def time_write(self):
        self.ds.to_netcdf(self.filename, compute=True)
        
    def teardown(self):
        if self.filename and os.path.exists(self.filename):
            os.remove(self.filename)