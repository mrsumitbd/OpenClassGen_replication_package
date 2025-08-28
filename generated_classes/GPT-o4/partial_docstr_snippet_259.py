class DataSource:
    '''
    Extracts raw data then restitute it as an arranged DataFrame.

    Args:
        preprocess (lambda): Preprocess DataFrame before transformation
    '''

    def __init__(self, fetch, preprocess=None):
        self.fetch = fetch
        self.preprocess = preprocess
        self._outputs = []
        self._context = None
        self._cached_df = None

    def add_output(self, name, function):
        '''
        Adds an output to the DataSource. The order in which the outputs are appended is important if previous outputs are reused.

        Args:
            name (str): Name of the output
            function (lambda): Function to apply to DataFrame

        Examples:
            >>> add_output('double', lambda df: 2 * df['number'])
        '''
        self._outputs.append((name, function))

    def transform(self, df):
        '''
        Transforms a DataFrame in place. Computes all outputs of the DataFrame.

        Args:
            df (pandas.DataFrame): DataFrame to transform.
        '''
        for name, func in self._outputs:
            df[name] = func(df)

    def get_dataframe(self, force_computation=False):
        '''
        Preprocesses then transforms the return of fetch().

        Args:
            force_computation (bool, optional) : Defaults to False. If set to True, forces the computation of DataFrame at each call.

        Returns:
            pandas.DataFrame: Preprocessed and transformed DataFrame.
        '''
        if force_computation or self._cached_df is None:
            df = self.fetch(self._context) if self._context is not None else self.fetch()
            if self.preprocess:
                df = self.preprocess(df)
            self.transform(df)
            self._cached_df = df
        return self._cached_df

    def set_context(self, context):
        '''
        Set context for runtime. Will be passed to fetch() function.

        Args:
            context (obj): Context to be passed to fetch().
        '''
        self._context = context