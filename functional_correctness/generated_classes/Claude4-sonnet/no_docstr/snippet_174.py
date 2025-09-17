class ToDict:
    def __init__(self):
        self.df_ints = None
        self.df_datetimelike = None

    def setup(self, orient):
        # Create DataFrame with integer data
        np.random.seed(42)
        data_ints = np.random.randint(0, 1000, size=(1000, 10))
        self.df_ints = pd.DataFrame(data_ints, columns=[f'col_{i}' for i in range(10)])
        
        # Create DataFrame with datetime-like data
        dates = pd.date_range('2020-01-01', periods=1000, freq='D')
        timestamps = pd.to_datetime(dates)
        timedeltas = pd.to_timedelta(np.arange(1000), unit='D')
        
        self.df_datetimelike = pd.DataFrame({
            'dates': dates,
            'timestamps': timestamps,
            'timedeltas': timedeltas,
            'periods': pd.period_range('2020-01', periods=1000, freq='D')
        })

    def time_to_dict_ints(self, orient):
        return self.df_ints.to_dict(orient=orient)

    def time_to_dict_datetimelike(self, orient):
        return self.df_datetimelike.to_dict(orient=orient)