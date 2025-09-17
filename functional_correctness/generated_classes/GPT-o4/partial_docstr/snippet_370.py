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
        self.id = str(uuid.uuid4())
        self.plans = plans if plans is not None else []
        self.success = False

    def __str__(self):
        return f"Goal(id={self.id}, name={self.name}, success={self.success})"

    def get_name(self):
        return self.name

    def find_best_plan(self):
        best = None
        best_score = None
        for plan in self.plans:
            score = getattr(plan, 'score', None)
            if score is None:
                try:
                    score = plan.evaluate()
                except Exception:
                    continue
            if best_score is None or score > best_score:
                best = plan
                best_score = score
        return best

    def check_for_success(self):
        return bool(self.success)