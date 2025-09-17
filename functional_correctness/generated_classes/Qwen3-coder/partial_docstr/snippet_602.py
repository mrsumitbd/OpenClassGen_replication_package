class SimpleTimeSeriesExtractor(object):
    '''
    This class will take a "simple" csv or excel file as input and out a timeseries, if there is a timeseries to be
    extracted.
    '''

    def __init__(self, csv_file_path: str):
        self.file_path = csv_file_path
        self.data = None
        self.time_series = None
        self.time_column = None
        self.value_columns = []

    def process(self):
        # Load the data
        self._load_data()
        
        # Identify time column and value columns
        self._identify_columns()
        
        # Extract time series
        if self.time_column and self.value_columns:
            self.time_series = self.data[[self.time_column] + self.value_columns]
            # Convert time column to datetime
            self.time_series[self.time_column] = pd.to_datetime(self.time_series[self.time_column])
            # Set time column as index
            self.time_series = self.time_series.set_index(self.time_column)
        
        return self.time_series

    def _load_data(self):
        file_extension = os.path.splitext(self.file_path)[1].lower()
        
        if file_extension == '.csv':
            self.data = pd.read_csv(self.file_path)
        elif file_extension in ['.xlsx', '.xls']:
            self.data = pd.read_excel(self.file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")

    def _identify_columns(self):
        if self.data is None:
            return
            
        # Try to identify time/date column
        for column in self.data.columns:
            # Check if column name suggests it's a time column
            col_name_lower = column.lower()
            if any(keyword in col_name_lower for keyword in ['date', 'time', 'datetime', 'timestamp']):
                self.time_column = column
                break
        
        # If no time column found by name, try to infer from data types
        if self.time_column is None:
            for column in self.data.columns:
                if self.data[column].dtype == 'object':
                    # Try to parse as datetime
                    try:
                        pd.to_datetime(self.data[column].iloc[:5])  # Test first 5 rows
                        self.time_column = column
                        break
                    except:
                        continue
        
        # Identify value columns (numeric columns excluding the time column)
        self.value_columns = []
        for column in self.data.columns:
            if column != self.time_column and pd.api.types.is_numeric_dtype(self.data[column]):
                self.value_columns.append(column)