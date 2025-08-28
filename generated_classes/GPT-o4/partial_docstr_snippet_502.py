class _CountTracker(object):
    '''Helper class to track counts of various document hierarchies in the corpus.
    For example, if the tokenizer can tokenize docs as (docs, paragraph, sentences, words), then this utility
    will track number of paragraphs, number of sentences within paragraphs and number of words within sentence.
    '''

    def __init__(self):
        self.last_indices = None
        self.counts = None
        self.local_counts = None

    def update(self, indices):
        '''Updates counts based on indices. The algorithm tracks the index change at i and
           update global counts for all indices beyond i with local counts tracked so far.
        '''
        # make a list copy
        indices = list(indices)
        D = len(indices)

        # first call: initialize
        if self.last_indices is None:
            # we track levels 1..D-1, so counts and locals have length D-1
            self.counts = [[] for _ in range(D-1)]
            # on first token we have seen one unit at each level
            self.local_counts = [1] * (D-1)
            self.last_indices = indices
            return

        # find the first level that changed
        for k in range(D):
            if indices[k] != self.last_indices[k]:
                break
        else:
            # no change => nothing to do
            return

        # if we changed at level k < D-1, flush all deeper-level counts j>=k
        if k < D-1:
            # j runs over  D-2, D-3, ..., k
            for j in range(D-2, k-1, -1):
                self.counts[j].append(self.local_counts[j])
                self.local_counts[j] = 0

        # now increment the count of the just-finished level
        # (for k>0 it is local_counts[k-1], for k=0 nothing)
        if k > 0:
            self.local_counts[k-1] += 1

        # roll forward
        self.last_indices = indices

    def finalize(self):
        '''This will add the very last document to counts. We also get rid of counts[0] since that
           represents document level which doesnt come under anything else. We also convert all count
           values to numpy arrays so that stats can be computed easily.
        '''
        if self.local_counts is None:
            return

        # flush whatever remains
        for j in range(len(self.local_counts)-1, -1, -1):
            self.counts[j].append(self.local_counts[j])

        # drop the top‐level (doc‐level) counts
        self.counts.pop(0)

        # convert to numpy arrays
        self.counts = [np.array(c) for c in self.counts]

        return self.counts