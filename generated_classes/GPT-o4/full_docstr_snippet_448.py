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
        funcs = {"cross_entropy", "softmax_cross_entropy", "mse"}
        if lfunc not in funcs:
            raise ValueError(f"Unsupported loss function '{lfunc}'. Valid options: {funcs}")
        self.lfunc = lfunc
        self.summary = summary
        self.name = name

    def compile(self, mod_y, ref_y, regterm=None):
        '''Compute the loss function tensor.

        Parameters
        ----------

        mod_y : tf.Tensor
            model output tensor

        ref_y : tf.Tensor
            reference input tensor

        regterm : tf.Tensor, optional (default = None)
            Regularization term tensor

        Returns
        -------

        Loss function tensor.
        '''
        if self.lfunc == "cross_entropy":
            per_example = tf.nn.sigmoid_cross_entropy_with_logits(labels=ref_y, logits=mod_y)
            loss = tf.reduce_mean(per_example, name=self.name)
        elif self.lfunc == "softmax_cross_entropy":
            per_example = tf.nn.softmax_cross_entropy_with_logits(labels=ref_y, logits=mod_y)
            loss = tf.reduce_mean(per_example, name=self.name)
        elif self.lfunc == "mse":
            loss = tf.reduce_mean(tf.square(mod_y - ref_y), name=self.name)
        else:
            # Should not happen due to check in __init__
            raise ValueError(f"Unknown loss function '{self.lfunc}'")

        if regterm is not None:
            loss = tf.add(loss, regterm, name=self.name + "_with_reg")

        if self.summary:
            tf.summary.scalar(self.name, loss)

        return loss