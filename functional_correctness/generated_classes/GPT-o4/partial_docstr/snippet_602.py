class SimpleTimeSeriesExtractor(object):
    '''
    This class will take a "simple" csv or excel file as input and out a timeseries, if there is a timeseries to be
    extracted.
    '''

    def __init__(self, csv_file_path: str):
        self.file_path = csv_file_path
        self.df = None
        self.timeseries = None

    def process(self):
        # Load file
        _, ext = os.path.splitext(self.file_path.lower())
        if ext in ['.xls', '.xlsx']:
            self.df = pd.read_excel(self.file_path)
        elif ext in ['.csv', '.txt']:
            self.df = pd.read_csv(self.file_path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

        if self.df.empty:
            raise ValueError("Input file is empty")

        # Identify datetime-like columns
        date_scores = {}
        for col in self.df.columns:
            parsed = pd.to_datetime(self.df[col], errors='coerce', infer_datetime_format=True)
            non_null = parsed.notna().sum()
            date_scores[col] = non_null

        # pick the column with highest parse count, require at least one parse
        date_col, max_count = max(date_scores.items(), key=lambda kv: kv[1])
        if max_count == 0:
            raise ValueError("No datetime-like column found")

        dates = pd.to_datetime(self.df[date_col], errors='coerce', infer_datetime_format=True)

        # Identify numeric columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        if not numeric_cols:
            # try converting non-numeric to numeric
            for col in self.df.columns:
                coerced = pd.to_numeric(self.df[col], errors='coerce')
                if coerced.notna().sum() > 0:
                    numeric_cols.append(col)
            numeric_cols = list(dict.fromkeys(numeric_cols))
        if not numeric_cols:
            raise ValueError("No numeric column found")

        # choose first numeric column
        value_col = numeric_cols[0]
        values = pd.to_numeric(self.df[value_col], errors='coerce')

        # build timeseries
        ts = pd.Series(data=values.values, index=dates.values)
        ts = ts[~ts.index.isna()]
        ts.index = pd.to_datetime(ts.index)
        ts = ts.sort_index()

        self.timeseries = ts
        return ts