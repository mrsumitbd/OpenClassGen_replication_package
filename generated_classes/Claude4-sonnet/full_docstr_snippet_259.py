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
        # Read the log file to extract header information
        with open(log_filename, 'r') as f:
            lines = f.readlines()
        
        # Parse header lines to get column names and types
        column_names = None
        column_types = None
        separator = '\t'
        
        for line in lines:
            if line.startswith('#fields'):
                column_names = line.strip().split('\t')[1:]
            elif line.startswith('#types'):
                column_types = line.strip().split('\t')[1:]
            elif line.startswith('#separator'):
                separator = line.strip().split(' ')[1]
                if separator == '\\x09':
                    separator = '\t'
            elif not line.startswith('#'):
                break
        
        # Build Spark schema
        schema = self.build_spark_schema(column_names, column_types)
        
        # Read the CSV data
        df = self.spark.read.csv(
            log_filename,
            sep=separator,
            header=False,
            schema=schema,
            comment='#'
        )
        
        # Fill NA values if requested
        if fillna:
            # Replace '-' with None/null values
            for col_name in df.columns:
                df = df.withColumn(col_name, 
                    when(col(col_name) == '-', None).otherwise(col(col_name)))
            
            # Fill null values based on column type
            for field in df.schema.fields:
                if isinstance(field.dataType, StringType):
                    df = df.fillna('', subset=[field.name])
                elif isinstance(field.dataType, (IntegerType, LongType, DoubleType, FloatType)):
                    df = df.fillna(0, subset=[field.name])
                elif isinstance(field.dataType, BooleanType):
                    df = df.fillna(False, subset=[field.name])
        
        return df

    def build_spark_schema(self, column_names, column_types, verbose=False):
        '''Given a set of names and types, construct a dictionary to be used
           as the Spark read_csv dtypes argument'''
        
        # Mapping from Zeek types to Spark types
        type_mapping = {
            'bool': BooleanType(),
            'count': LongType(),
            'int': IntegerType(),
            'double': DoubleType(),
            'time': DoubleType(),
            'interval': DoubleType(),
            'string': StringType(),
            'addr': StringType(),
            'port': IntegerType(),
            'enum': StringType(),
            'set': StringType(),
            'vector': StringType(),
            'subnet': StringType()
        }
        
        fields = []
        for name, zeek_type in zip(column_names, column_types):
            # Handle vector types like vector[string]
            if zeek_type.startswith('vector[') or zeek_type.startswith('set['):
                spark_type = StringType()
            else:
                spark_type = type_mapping.get(zeek_type, StringType())
            
            fields.append(StructField(name, spark_type, True))
            
            if verbose:
                print(f"Column: {name}, Zeek Type: {zeek_type}, Spark Type: {spark_type}")
        
        return StructType(fields)