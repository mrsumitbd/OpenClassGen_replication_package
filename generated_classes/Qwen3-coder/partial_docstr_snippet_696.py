class QoIProcessor(object):
    '''
        Quality of Information processor based on a recurrent convolutional network.
        Supervised learning method that has been used to classify accelerometer signal (collected through the cloudUPDRS app) according to qulity.
        The method has been used in a binary fashion (good vs bad signals) but this can easily do multiclass classification.
        Initializing this processor will instantiate a model and the model uses the keras api: https://keras.io.

        :param input_shape: (optional) Shape of the input data, this has to be in 2d, without the minibatch size
        :type input_shape: tuple
        :param labels: (optional) Number of classes, this should be 1 for binary classification.
        :type labels: int
        :param output_activation: (optional) The activation function to use on the output data. For binary classification use 'sigmoid', for multiclass use 'softmax'
        :type output_activation: str


        :Examples:
         
        >>> import pdkit
        >>> qoi = pdkit.QoIProcessor()
        >>> qoi.model.fit(X, y)
    '''

    def __init__(self,
                 input_shape=(150, 4),
                 labels=1,
                 output_activation='sigmoid'):
        self.input_shape = input_shape
        self.labels = labels
        self.output_activation = output_activation
        
        # Build the model
        self.model = self._build_model()
    
    def _build_model(self):
        # Input layer
        inputs = keras.Input(shape=self.input_shape)
        
        # Convolutional layers
        conv1 = layers.Conv1D(32, 3, activation='relu', padding='same')(inputs)
        conv1 = layers.BatchNormalization()(conv1)
        conv1 = layers.Dropout(0.2)(conv1)
        
        conv2 = layers.Conv1D(64, 3, activation='relu', padding='same')(conv1)
        conv2 = layers.BatchNormalization()(conv2)
        conv2 = layers.Dropout(0.2)(conv2)
        
        conv3 = layers.Conv1D(128, 3, activation='relu', padding='same')(conv2)
        conv3 = layers.BatchNormalization()(conv3)
        conv3 = layers.Dropout(0.2)(conv3)
        
        # Recurrent layer
        lstm = layers.LSTM(64, return_sequences=False)(conv3)
        lstm = layers.Dropout(0.2)(lstm)
        
        # Dense layers
        dense1 = layers.Dense(32, activation='relu')(lstm)
        dense1 = layers.Dropout(0.2)(dense1)
        
        # Output layer
        outputs = layers.Dense(self.labels, activation=self.output_activation)(dense1)
        
        # Create model
        model = keras.Model(inputs=inputs, outputs=outputs)
        
        # Compile model
        if self.output_activation == 'sigmoid':
            model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        else:
            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        
        return model

    def window_data(self, x, y=None, window_size=100, overlap=10):
        # Calculate step size
        step_size = window_size - overlap
        
        # Handle case where step_size is <= 0
        if step_size <= 0:
            step_size = 1
            
        # Calculate number of windows
        num_windows = max(0, (len(x) - window_size) // step_size + 1)
        
        if num_windows <= 0:
            # Return empty arrays with correct shape
            windowed_x = np.empty((0, window_size, x.shape[1])) if len(x.shape) > 1 else np.empty((0, window_size))
            if y is not None:
                windowed_y = np.empty((0,)) if len(y.shape) == 1 else np.empty((0, y.shape[1]))
                return windowed_x, windowed_y
            else:
                return windowed_x
        
        # Create windows for x
        windowed_x = []
        for i in range(num_windows):
            start_idx = i * step_size
            end_idx = start_idx + window_size
            if end_idx <= len(x):
                windowed_x.append(x[start_idx:end_idx])
        
        windowed_x = np.array(windowed_x)
        
        # If y is provided, create corresponding windows
        if y is not None:
            windowed_y = []
            for i in range(num_windows):
                start_idx = i * step_size
                end_idx = start_idx + window_size
                if end_idx <= len(x):
                    # For labels, take the label at the end of the window or majority vote
                    windowed_y.append(y[end_idx - 1] if end_idx - 1 < len(y) else y[-1])
            
            windowed_y = np.array(windowed_y)
            return windowed_x, windowed_y
        else:
            return windowed_x