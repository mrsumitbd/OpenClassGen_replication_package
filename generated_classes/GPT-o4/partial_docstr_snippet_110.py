class Space(object):
    '''
    A space is a description of the computation space for a specific CSP.
    '''

    def __init__(self, variables, constraints):
        '''
        Create a new Space for a CSP

        :param variables: The variables of the CSP
        :type variables: sequence of Variables
        :param constraints: The constraints of the CSP
        :type constraints: sequence of Constraints
        '''
        self.variables = list(variables)
        self.constraints = list(constraints)

    def is_discrete(self):
        '''
        Return whether this space is discrete
        '''
        return all(var.is_discrete() for var in self.variables)

    def consistent(self, lab):
        '''
        Check whether the labeling is consistent with all constraints
        '''
        for c in self.constraints:
            if not c.consistent(lab):
                return False
        return True

    def satisfied(self, lab):
        '''
        Check whether the labeling satisfies all constraints
        '''
        # all variables must be assigned
        for v in self.variables:
            if v not in lab:
                return False
        # all constraints must be satisfied
        for c in self.constraints:
            if not c.satisfied(lab):
                return False
        return True