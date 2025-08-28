class QoIProcessor(object):
    '''
        Quality of Information processor based on a recurrent convolutional network.
    '''
    def __init__(self,
                 input_shape=(150, 4),
                 labels=1,
                 output_activation='sigmoid'):
        self.input_shape = input_shape
        self.labels = labels
        self.output_activation = output_activation

        inp = Input(shape=self.input_shape)
        x = Conv1D(32, 3, padding='same')(inp)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = MaxPooling1D(2)(x)

        x = Conv1D(64, 3, padding='same')(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = MaxPooling1D(2)(x)

        x = LSTM(100, return_sequences=False)(x)
        x = Dropout(0.5)(x)

        x = Dense(50, activation='relu')(x)
        x = Dropout(0.5)(x)

        out = Dense(self.labels, activation=self.output_activation)(x)

        self.model = Model(inputs=inp, outputs=out)

        if self.labels == 1:
            loss = 'binary_crossentropy'
        else:
            loss = 'categorical_crossentropy'

        self.model.compile(optimizer=Adam(),
                           loss=loss,
                           metrics=['accuracy'])

    def window_data(self, x, y=None, window_size=100, overlap=10):
        '''
            Slide a window over data x (and optional labels y).
        '''
        def _single_window(x_arr, y_val):
            x_arr = np.asarray(x_arr)
            T = x_arr.shape[0]
            step = window_size - overlap
            if step <= 0:
                raise ValueError("overlap must be less than window_size")
            windows = []
            labels = []
            idx = 0
            while idx + window_size <= T:
                win = x_arr[idx:idx + window_size]
                windows.append(win)
                if y_val is not None:
                    if np.ndim(y_val) == 0:
                        labels.append(y_val)
                    else:
                        y_arr = np.asarray(y_val)
                        if y_arr.ndim == 1 and len(y_arr) == T:
                            labels.append(y_arr[idx + window_size - 1])
                        else:
                            raise ValueError("y array length must match x length when 1D")
                idx += step
            Xw = np.stack(windows) if windows else np.empty((0, window_size) + x_arr.shape[1:])
            if y_val is None:
                return Xw, None
            yw = np.array(labels)
            return Xw, yw

        # handle list/tuple of sequences
        if isinstance(x, (list, tuple)):
            X_list = []
            Y_list = []
            if y is not None:
                if not isinstance(y, (list, tuple)) or len(y) != len(x):
                    raise ValueError("when x is list, y must be list of same length")
            y_iter = y if y is not None else [None] * len(x)
            for xi, yi in zip(x, y_iter):
                Xw, yw = self.window_data(xi, yi, window_size, overlap)
                X_list.append(Xw)
                if yw is not None:
                    Y_list.append(yw)
            X_all = np.vstack(X_list) if X_list else np.empty((0, window_size) + np.asarray(x[0]).shape[1:])
            if y is None:
                return X_all
            Y_all = np.hstack(Y_list) if Y_list else np.empty((0,))
            return X_all, Y_all

        # single sequence
        Xw, yw = _single_window(x, y)
        if y is None:
            return Xw
        return Xw, yw