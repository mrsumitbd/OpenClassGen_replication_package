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
        # sort by decreasing length (assumes each match is (start, end, ...) or [start, end, ...])
        sorted_matches = sorted(
            self.template_matches,
            key=lambda m: (m[1] - m[0]) if len(m) >= 2 else 0,
            reverse=True
        )

        for match in sorted_matches:
            start, end = match[0], match[1]
            # check if this match is contained in any already selected maximal match
            contained = any(
                sel[0] <= start and sel[1] >= end
                for sel in self.maximal_matches
            )
            if not contained:
                self.maximal_matches.append(match)

        return self.maximal_matches