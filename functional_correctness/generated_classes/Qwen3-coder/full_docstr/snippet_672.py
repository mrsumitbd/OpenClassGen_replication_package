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
        self._rules = rules
        self._index = 0

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
        if self._index >= self._rules.numRules:
            raise StopIteration
        
        rule = self._rules.get(self._index)
        self._index += 1
        return rule