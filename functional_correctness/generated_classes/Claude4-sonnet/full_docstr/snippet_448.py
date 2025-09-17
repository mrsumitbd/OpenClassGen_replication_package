class Loss(object):
    '''Collection of loss functions.'''

    def __init__(self, lfunc, summary=True, name="loss"):
        '''Constructor.

        Parameters
        ----------

        lfunc : str
            Loss function type. Types supported:
            "cross_entropy", "softmax_cross_entropy" and "mse".

        summary : bool, optional (default = True)
            Whether to attach a tf scalar summary to the op.

        name : str, optional (default = "loss")
            Name for the loss op.
        '''
        self.lfunc = lfunc
        self.summary = summary
        self.name = name

    def compile(self, mod_y, ref_y, regterm=None):
        '''Compute the loss function tensor.

        Parameters
        ----------

        mode_y : tf.Tensor
            model output tensor

        ref_y : tf.Tensor
            reference input tensor

        regterm : tf.Tensor, optional (default = None)
            Regularization term tensor

        Returns
        -------

        Loss function tensor.
        '''
        with tf.name_scope(self.name):
            if self.lfunc == "cross_entropy":
                loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
                    logits=mod_y, labels=ref_y))
            elif self.lfunc == "softmax_cross_entropy":
                loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
                    logits=mod_y, labels=ref_y))
            elif self.lfunc == "mse":
                loss = tf.reduce_mean(tf.square(mod_y - ref_y))
            else:
                raise ValueError(f"Unsupported loss function: {self.lfunc}")
            
            if regterm is not None:
                loss = loss + regterm
            
            if self.summary:
                tf.summary.scalar(self.name, loss)
            
            return loss