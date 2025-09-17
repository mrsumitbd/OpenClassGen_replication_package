class ValueNetworkMixin:
    '''Assigns the `_value()` method to a TorchPolicy.

    This way, Policy can call `_value()` to get the current VF estimate on a
    single(!) observation (as done in `postprocess_trajectory_fn`).
    Note: When doing this, an actual forward pass is being performed.
    This is different from only calling `model.value_function()`, where
    the result of the most recent forward pass is being used to return an
    already calculated tensor.
    '''

    def __init__(self, config):
        if config.get("use_critic", True):
            def value(**input_dict):
                input_dict = self._lazy_tensor_dict(input_dict)
                model_out, _ = self.model(input_dict)
                return self.model.value_function()[0]
        else:
            def value(**input_dict):
                return 0.0
        
        self._value = value

    def extra_action_out(self, input_dict, state_batches, model, action_dist):
        '''Defines extra fetches per action computation.

        Args:
            input_dict (Dict[str, TensorType]): The input dict used for the action
                computing forward pass.
            state_batches (List[TensorType]): List of state tensors (empty for
                non-RNNs).
            model (ModelV2): The Model object of the Policy.
            action_dist: The instantiated distribution
                object, resulting from the model's outputs and the given
                distribution class.

        Returns:
            Dict[str, TensorType]: Dict with extra tf fetches to perform per
                action computation.
        '''
        return {"vf_preds": model.value_function()}