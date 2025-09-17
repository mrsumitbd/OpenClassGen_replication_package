class SimpleTimeSeriesExtractor(object):
    '''
    This class will take a "simple" csv or excel file as input and out a timeseries, if there is a timeseries to be
    extracted.
    '''

    def __init__(self, csv_file_path: str):
        self.csv_file_path = csv_file_path
        self.data = None
        self.timeseries = None

    def process(self):
        if not os.path.exists(self.csv_file_path):
            raise FileNotFoundError(f"File not found: {self.csv_file_path}")
        
        file_extension = os.path.splitext(self.csv_file_path)[1].lower()
        
        try:
            if file_extension == '.csv':
                self.data = pd.read_csv(self.csv_file_path)
            elif file_extension in ['.xlsx', '.xls']:
                self.data = pd.read_excel(self.csv_file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")
        
        if self.data.empty:
            return None
        
        date_column = None
        value_column = None
        
        for col in self.data.columns:
            if self._is_date_column(self.data[col]):
                date_column = col
                break
        
        if date_column is None:
            return None
        
        numeric_columns = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) == 0:
            return None
        
        value_column = numeric_columns[0]
        
        try:
            df_clean = self.data[[date_column, value_column]].dropna()
            df_clean[date_column] = pd.to_datetime(df_clean[date_column])
            df_clean = df_clean.sort_values(date_column)
            df_clean.set_index(date_column, inplace=True)
            
            self.timeseries = df_clean[value_column]
            return self.timeseries
        except Exception:
            return None
    
    def _is_date_column(self, series):
        if series.dtype == 'datetime64[ns]':
            return True
        
        non_null_series = series.dropna()
        if len(non_null_series) == 0:
            return False
        
        sample_size = min(10, len(non_null_series))
        sample = non_null_series.head(sample_size)
        
        date_count = 0
        for value in sample:
            if self._is_date_string(str(value)):
                date_count += 1
        
        return date_count / sample_size >= 0.7
    
    def _is_date_string(self, value_str):
        date_patterns = [
            '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d',
            '%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M:%S',
            '%Y-%m', '%m/%Y', '%Y'
        ]
        
        for pattern in date_patterns:
            try:
                datetime.strptime(value_str, pattern)
                return True
            except ValueError:
                continue
        
        try:
            pd.to_datetime(value_str)
            return True
        except (ValueError, TypeError):
            return False