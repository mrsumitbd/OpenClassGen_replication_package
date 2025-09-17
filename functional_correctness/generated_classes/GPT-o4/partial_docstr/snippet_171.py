class ValueNetworkMixin:
    """Assigns the `_value()` method to a TorchPolicy.

    This way, Policy can call `_value()` to get the current VF estimate on a
    single(!) observation (as done in `postprocess_trajectory_fn`).
    Note: When doing this, an actual forward pass is being performed.
    This is different from only calling `model.value_function()`, where
    the result of the most recent forward pass is being used to return an
    already calculated tensor.
    """

    def __init__(self, config):
        def _value(**input_dict):
            device = getattr(self, "device", torch.device("cpu"))
            # Build batched input dict
            batched = {}
            state_batches = []
            for k, v in input_dict.items():
                if k == "state":
                    for s in v:
                        if isinstance(s, np.ndarray):
                            t = torch.from_numpy(s).to(device)
                        else:
                            t = s.to(device)
                        state_batches.append(t.unsqueeze(0))
                elif k == "obs":
                    if isinstance(v, np.ndarray):
                        t = torch.from_numpy(v).to(device)
                    else:
                        t = v.to(device)
                    batched["obs"] = t.unsqueeze(0)
                elif k == "prev_action":
                    if isinstance(v, np.ndarray):
                        t = torch.from_numpy(v).to(device)
                    else:
                        t = v.to(device)
                    batched["prev_action"] = t.unsqueeze(0)
                elif k == "prev_reward":
                    if isinstance(v, (float, int, np.generic)):
                        t = torch.tensor([v], dtype=torch.float32, device=device)
                    elif isinstance(v, np.ndarray):
                        t = torch.from_numpy(v).to(device)
                        t = t.unsqueeze(0)
                    else:
                        t = v.to(device).unsqueeze(0)
                    batched["prev_reward"] = t
                else:
                    # Other inputs
                    if isinstance(v, np.ndarray):
                        t = torch.from_numpy(v).to(device).unsqueeze(0)
                        batched[k] = t
                    elif isinstance(v, torch.Tensor):
                        batched[k] = v.to(device).unsqueeze(0)
                    else:
                        batched[k] = v
            # Forward pass
            out, new_states, extra = self.model(batched, state_batches, explore=False)
            vf = self.model.value_function()
            # Return single value
            val = vf[0]
            return val.cpu().detach().numpy()
        self._value = _value
        self.value = _value
        self.value_exploration = _value

    def extra_action_out(self, input_dict, state_batches, model, action_dist):
        """Defines extra fetches per action computation."""
        vf = model.value_function()
        return {"vf_preds": vf}