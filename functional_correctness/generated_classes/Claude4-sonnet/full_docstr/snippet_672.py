class AssociationRulesIterator(object):
    '''
    Iterator for weka.associations.AssociationRules class.
    '''

    def __init__(self, rules):
        '''
        Initializes with the rules.

        :param rules: the rules to use
        :type rules: AssociationRules
        '''
        self.rules = rules
        self.index = 0

    def __iter__(self):
        '''
        Returns itself.
        '''
        return self

    def __next__(self):
        '''
        Returns the next rule.

        :return: the next rule object
        :rtype: AssociationRule
        '''
        if self.index >= len(self.rules):
            raise StopIteration
        rule = self.rules[self.index]
        self.index += 1
        return rule