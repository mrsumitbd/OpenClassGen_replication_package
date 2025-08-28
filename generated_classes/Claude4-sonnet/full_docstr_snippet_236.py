class MaximalMatches:
    '''
    Class MaximalMatches allows to sort and store the maximal matches from the list
    of matches obtained with the template matching algorithm.
    '''

    def __init__(self, template_matches):
        '''
        Initialize MaximalMatches with the necessary arguments.
        Args:
            template_matches (list): list of matches obtained from running the algorithm.
        '''
        self.template_matches = template_matches
        self.maximal_matches = []

    def run_maximal_matches(self):
        '''
        Method that extracts and stores maximal matches in decreasing length order.
        '''
        # Sort matches by length in decreasing order
        sorted_matches = sorted(self.template_matches, key=len, reverse=True)
        
        for match in sorted_matches:
            is_maximal = True
            # Check if current match is contained in any already selected maximal match
            for maximal_match in self.maximal_matches:
                if self._is_submatch(match, maximal_match):
                    is_maximal = False
                    break
            
            if is_maximal:
                self.maximal_matches.append(match)
    
    def _is_submatch(self, match1, match2):
        '''
        Helper method to check if match1 is a submatch of match2.
        '''
        if len(match1) > len(match2):
            return False
        
        match1_str = ''.join(str(x) for x in match1)
        match2_str = ''.join(str(x) for x in match2)
        
        return match1_str in match2_str