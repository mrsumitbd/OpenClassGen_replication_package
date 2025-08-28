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
        # Sort matches by length in descending order
        sorted_matches = sorted(self.template_matches, key=lambda x: len(x) if hasattr(x, '__len__') else 1, reverse=True)
        
        # Extract maximal matches
        maximal_matches = []
        for match in sorted_matches:
            is_maximal = True
            # Check if current match is contained in any already selected maximal match
            for maximal_match in maximal_matches:
                if self._is_contained(match, maximal_match):
                    is_maximal = False
                    break
            if is_maximal:
                maximal_matches.append(match)
        
        self.maximal_matches = maximal_matches

    def _is_contained(self, match, maximal_match):
        '''
        Helper method to check if a match is contained within a maximal match.
        '''
        # This is a generic implementation - can be customized based on match structure
        if isinstance(match, str) and isinstance(maximal_match, str):
            return match in maximal_match
        elif hasattr(match, '__iter__') and hasattr(maximal_match, '__iter__'):
            # For sequences, check if match is a subsequence of maximal_match
            match_iter = iter(match)
            maximal_iter = iter(maximal_match)
            try:
                match_item = next(match_iter)
                for maximal_item in maximal_iter:
                    if maximal_item == match_item:
                        match_item = next(match_iter)
            except StopIteration:
                return True
            return False
        else:
            return False