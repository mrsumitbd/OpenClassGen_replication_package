class LogToSparkDF(object):
    '''LogToSparkDF: Converts a Zeek log to a Spark DataFrame'''
    def __init__(self, spark):
        '''Initialize the LogToSparkDF class'''
        self.spark = spark

    def create_dataframe(self, log_filename, fillna=True):
        ''' Create a Spark dataframe from a Bro/Zeek log file
            Args:
               log_filename (string): The full path to the Zeek log
               fillna (bool): Fill in NA/NaN values (default=True)
        '''
        sep = None
        empty_field = None
        unset_field = None
        fields = []
        types = []
        with open(log_filename, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.startswith('#'):
                    break
                parts = line.rstrip('\n').split(' ', 1)
                tag = parts[0]
                if len(parts) > 1:
                    val = parts[1]
                else:
                    continue
                if tag == '#separator':
                    sep = val.encode('utf-8').decode('unicode_escape')
                elif tag == '#empty_field':
                    empty_field = val
                elif tag == '#unset_field':
                    unset_field = val
                elif tag == '#fields':
                    fields = val.split(sep)
                elif tag == '#types':
                    types = val.split(sep)
        if sep is None:
            sep = '\t'
        if unset_field is None:
            unset_field = '-'
        schema = self.build_spark_schema(fields, types)
        df = (
            self.spark.read
                .options(header=False, sep=sep, comment='#', nullValue=unset_field)
                .schema(schema)
                .csv(log_filename)
                .toDF(*fields)
        )
        if fillna:
            fill_map = {}
            for name, t in zip(fields, types):
                tl = t.lower()
                if tl in ('count', 'int', 'uint', 'port'):
                    fill_map[name] = 0
                elif tl == 'double' or tl == 'interval':
                    fill_map[name] = 0.0
                elif tl == 'bool':
                    fill_map[name] = False
                else:
                    fill_map[name] = ''  # strings and others
            df = df.fillna(fill_map)
        return df

    def build_spark_schema(self, column_names, column_types, verbose=False):
        '''Given a set of names and types, construct a Spark StructType schema'''
        mapping = {
            'string': StringType(),
            'enum': StringType(),
            'sub': StringType(),
            'file': StringType(),
            'pattern': StringType(),
            'addr': StringType(),
            'bool': BooleanType(),
            'count': LongType(),
            'int': LongType(),
            'uint': LongType(),
            'port': LongType(),
            'double': DoubleType(),
            'time': TimestampType(),
            'interval': DoubleType()
        }
        fields = []
        for name, t in zip(column_names, column_types):
            spark_type = mapping.get(t.lower(), StringType())
            fields.append(StructField(name, spark_type, nullable=True))
            if verbose and t.lower() not in mapping:
                print(f"Type '{t}' not in mapping, defaulting to StringType for column '{name}'")
        return StructType(fields)