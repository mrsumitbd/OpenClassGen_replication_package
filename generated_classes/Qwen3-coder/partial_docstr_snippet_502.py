class _CountTracker(object):
    '''Helper class to track counts of various document hierarchies in the corpus.
    For example, if the tokenizer can tokenize docs as (docs, paragraph, sentences, words), then this utility
    will track number of paragraphs, number of sentences within paragraphs and number of words within sentence.
    '''

    def __init__(self):
        self.counts = {}
        self.last_indices = None

    def update(self, indices):
        '''Updates counts based on indices. The algorithm tracks the index change at i and
        update global counts for all indices beyond i with local counts tracked so far.
        '''
        if self.last_indices is None:
            self.last_indices = indices[:]
            return
            
        # Find the first index where indices differ
        change_point = 0
        for i in range(min(len(indices), len(self.last_indices))):
            if indices[i] != self.last_indices[i]:
                change_point = i
                break
        else:
            # If one is prefix of another or they are identical
            change_point = min(len(indices), len(self.last_indices))
            
        # Update counts for all levels beyond the change point
        for i in range(change_point, len(self.last_indices)):
            if i not in self.counts:
                self.counts[i] = []
            # Count is the difference in the index at position i-1 (or 0 if i=0)
            if i == 0:
                count = self.last_indices[i] + 1
            else:
                count = self.last_indices[i] + 1
            self.counts[i].append(count)
            
        self.last_indices = indices[:]

    def finalize(self):
        '''This will add the very last document to counts. We also get rid of counts[0] since that
        represents document level which doesnt come under anything else. We also convert all count
        values to numpy arrays so that stats can be computed easily.
        '''
        if self.last_indices is not None:
            # Add the final counts
            for i in range(len(self.last_indices)):
                if i not in self.counts:
                    self.counts[i] = []
                if i == 0:
                    count = self.last_indices[i] + 1
                else:
                    count = self.last_indices[i] + 1
                self.counts[i].append(count)
        
        # Remove counts[0] as it represents document level
        if 0 in self.counts:
            del self.counts[0]
            
        # Convert all counts to numpy arrays
        for key in self.counts:
            self.counts[key] = np.array(self.counts[key])