class MatchingScenariosList:
    '''
    Object to define a list of MatchingScenarios, with method to append
    and pop elements.
    '''

    def __init__(self):
        '''
        Create an empty MatchingScenariosList.
        '''
        self._scenarios = []

    def append_scenario(self, matching):
        '''
        Append a scenario to the list.
        Args:
            matching (MatchingScenarios): a scenario of match.
        '''
        self._scenarios.append(matching)

    def pop_scenario(self):
        '''
        Pop the first scenario of the list.
        Returns:
            MatchingScenarios: a scenario of match.
        '''
        return self._scenarios.pop(0)