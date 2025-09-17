class DataSource:
    '''
    Extracts raw data then restitute it as an arranged DataFrame.

    Args:
        preprocess (lambda): Preprocess DataFrame before transformation
    '''

    def __init__(self, fetch, preprocess=None):
        self.fetch = fetch
        self.preprocess = preprocess
        self.outputs = []
        self.context = None
        self._cached_dataframe = None

    def add_output(self, name, function):
        '''
        Adds an output to the DataSource. The order in which the outputs are appended is important if previous outputs are reused.

        Args:
            name (str): Name of the output
            function (lambda): Function to apply to DataFrame

        Examples:
            >>> add_output('double', lambda df: 2 * df['number'])
        '''
        self.outputs.append((name, function))

    def transform(self, df):
        '''
        Transforms a DataFrame in place. Computes all outputs of the DataFrame.

        Args:
            df (pandas.DataFrame): DataFrame to transform.
        '''
        for name, function in self.outputs:
            df[name] = function(df)

    def get_dataframe(self, force_computation=False):
        '''
        Preprocesses then transforms the return of fetch().

        Args:
            force_computation (bool, optional) : Defaults to False. If set to True, forces the computation of DataFrame at each call.

        Returns:
            pandas.DataFrame: Preprocessed and transformed DataFrame.
        '''
        if not force_computation and self._cached_dataframe is not None:
            return self._cached_dataframe.copy()

        # Fetch raw data
        if self.context is not None:
            df = self.fetch(self.context)
        else:
            df = self.fetch()

        # Preprocess if needed
        if self.preprocess is not None:
            df = self.preprocess(df)

        # Transform DataFrame
        self.transform(df)

        # Cache the result
        self._cached_dataframe = df.copy()
        
        return df

    def set_context(self, context):
        '''
        Set context for runtime. Will be passed to fetch() function.

        Args:
            context (obj): Context to be passed to fetch().
        '''
        self.context = context
        # Invalidate cache when context changes
        self._cached_dataframe = None