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
        self.variables = variables
        self.constraints = constraints

    def is_discrete(self):
        '''
        Return whether this space is discrete
        '''
        # Assuming all CSP spaces are discrete by default
        # This could be extended to check variable domains
        return True

    def consistent(self, lab):
        '''
        Check whether the labeling is consistent with all constraints
        '''
        for constraint in self.constraints:
            if not constraint.consistent(lab):
                return False
        return True

    def satisfied(self, lab):
        '''
        Check whether the labeling satisfies all constraints
        '''
        for constraint in self.constraints:
            if not constraint.satisfied(lab):
                return False
        return True