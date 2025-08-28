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
        # Read the log file to get column names and types
        with open(log_filename, 'r') as f:
            lines = f.readlines()
        
        # Find the header lines
        fields_line = None
        types_line = None
        
        for line in lines:
            if line.startswith('#fields'):
                fields_line = line.strip()
            elif line.startswith('#types'):
                types_line = line.strip()
            if fields_line and types_line:
                break
        
        if not fields_line or not types_line:
            raise ValueError("Could not find #fields and #types lines in log file")
        
        # Extract column names and types
        column_names = fields_line.split('\t')[1:]  # Skip '#fields'
        column_types = types_line.split('\t')[1:]   # Skip '#types'
        
        # Build Spark schema
        schema_dict = self.build_spark_schema(column_names, column_types)
        
        # Read the actual data (skip comment lines)
        data_lines = []
        for line in lines:
            if not line.startswith('#'):
                data_lines.append(line.strip())
        
        # Create RDD from data lines
        rdd = self.spark.sparkContext.parallelize(data_lines)
        rdd = rdd.map(lambda line: line.split('\t'))
        
        # Create DataFrame
        df = self.spark.createDataFrame(rdd, list(schema_dict.keys()))
        
        # Fill NA/NaN values if requested
        if fillna:
            df = df.fillna('')
        
        return df

    def build_spark_schema(self, column_names, column_types, verbose=False):
        '''Given a set of names and types, construct a dictionary to be used
           as the Spark read_csv dtypes argument'''
        # Mapping from Zeek types to Spark types
        type_mapping = {
            'bool': 'boolean',
            'count': 'integer',
            'int': 'integer',
            'double': 'double',
            'time': 'double',
            'interval': 'double',
            'string': 'string',
            'addr': 'string',
            'port': 'integer',
            'subnet': 'string',
            'enum': 'string',
            'function': 'string',
            'record': 'string',
            'vector': 'string',
            'set': 'string',
            'table': 'string'
        }
        
        schema_dict = {}
        for i, (name, zeek_type) in enumerate(zip(column_names, column_types)):
            # Handle complex types (vectors, sets, etc.) by treating as string
            spark_type = type_mapping.get(zeek_type, 'string')
            schema_dict[name] = spark_type
            
            if verbose:
                print(f"Column '{name}': Zeek type '{zeek_type}' -> Spark type '{spark_type}'")
        
        return schema_dict