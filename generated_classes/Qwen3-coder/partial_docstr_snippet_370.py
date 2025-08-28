class Goal(object):
    ''' 
    base class for handling various goals for AIKIF, usually in string format, but
    has methods to load/save and compare.
    name: title of the goal
    id: id of the goal - obtain from Goals class or database
    success: whether the goal has been successful or not
    '''

    def __init__(self, name='New Goal', plans=None):
        self.name = name
        self.id = None
        self.success = False
        self.plans = plans if plans is not None else []

    def __str__(self):
        return f"Goal(name='{self.name}', id={self.id}, success={self.success})"

    def get_name(self):
        return self.name

    def find_best_plan(self):
        '''
        Main logic in class which tries different plans according to a
        strategy (no idea how as yet) on test data, then runs that plan
        to simulate a result
        '''
        # Base implementation - simply return the first plan if available
        if self.plans:
            return self.plans[0]
        return None

    def check_for_success(self):
        ''' do the checking to see if goal has reached its target
        This is usually overloaded by other classes, and for numerical
        tests is simply if maximise == True:
                            if TARGET > CURRENT:
                                return True
                            else:
                                return False
                        else:
                            if TARGET < CURRENT:
                                return True
                            else:
                                return False
        '''
        # Base implementation - return the current success status
        return self.success