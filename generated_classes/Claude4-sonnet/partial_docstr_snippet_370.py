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
        self.current_plan = None
        self.target = None
        self.current = None
        self.maximise = True

    def __str__(self):
        return f"Goal: {self.name} (ID: {self.id}, Success: {self.success})"

    def get_name(self):
        return self.name

    def find_best_plan(self):
        '''
        Main logic in class which tries different plans according to a
        strategy (no idea how as yet) on test data, then runs that plan
        to simulate a result
        '''
        if not self.plans:
            return None
        
        best_plan = None
        best_score = None
        
        for plan in self.plans:
            score = self._evaluate_plan(plan)
            if best_score is None or score > best_score:
                best_score = score
                best_plan = plan
        
        self.current_plan = best_plan
        return best_plan

    def _evaluate_plan(self, plan):
        return 0

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
        if self.target is None or self.current is None:
            return False
        
        if self.maximise:
            if self.current >= self.target:
                self.success = True
                return True
            else:
                self.success = False
                return False
        else:
            if self.current <= self.target:
                self.success = True
                return True
            else:
                self.success = False
                return False