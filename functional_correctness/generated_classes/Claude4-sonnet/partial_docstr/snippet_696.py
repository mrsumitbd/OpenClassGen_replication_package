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
        
        self.model = keras.Sequential([
            layers.Conv1D(32, 3, activation='relu', input_shape=input_shape),
            layers.Conv1D(64, 3, activation='relu'),
            layers.MaxPooling1D(2),
            layers.Conv1D(128, 3, activation='relu'),
            layers.MaxPooling1D(2),
            layers.LSTM(64, return_sequences=True),
            layers.LSTM(32),
            layers.Dropout(0.5),
            layers.Dense(64, activation='relu'),
            layers.Dense(labels, activation=output_activation)
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy' if labels == 1 else 'categorical_crossentropy',
            metrics=['accuracy']
        )

    def window_data(self, x, y=None, window_size=100, overlap=10):
        step_size = window_size - overlap
        n_windows = (len(x) - window_size) // step_size + 1
        
        windowed_x = []
        for i in range(n_windows):
            start_idx = i * step_size
            end_idx = start_idx + window_size
            windowed_x.append(x[start_idx:end_idx])
        
        windowed_x = np.array(windowed_x)
        
        if y is not None:
            windowed_y = []
            for i in range(n_windows):
                start_idx = i * step_size
                end_idx = start_idx + window_size
                windowed_y.append(y[start_idx:end_idx])
            windowed_y = np.array(windowed_y)
            return windowed_x, windowed_y
        
        return windowed_x