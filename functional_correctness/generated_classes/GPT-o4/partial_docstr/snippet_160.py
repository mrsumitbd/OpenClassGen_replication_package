class BaseModder:
    '''
    Base class meant to modify simulation attributes mid-sim.

    Using @random_state ensures that sampling here won't be affected
    by sampling that happens outside of the modders.

    Args:
        sim (MjSim): simulation object

        random_state (RandomState): instance of np.random.RandomState, specific
            seed used to randomize these modifications without impacting other
            numpy seeds / randomizations
    '''

    def __init__(self, sim, random_state=None):
        self.sim = sim
        if random_state is None:
            self.random_state = np.random.RandomState()
        else:
            self.random_state = random_state

    def update_sim(self, sim):
        '''
        Setter function to update internal sim variable

        Args:
            sim (MjSim): MjSim object
        '''
        self.sim = sim

    @property
    def model(self):
        '''
        Returns:
            MjModel: Mujoco sim model
        '''
        return self.sim.model