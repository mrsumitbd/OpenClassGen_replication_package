class _CountTracker(object):
    '''Helper class to track counts of various document hierarchies in the corpus.
    For example, if the tokenizer can tokenize docs as (docs, paragraph, sentences, words), then this utility
    will track number of paragraphs, number of sentences within paragraphs and number of words within sentence.
    '''

    def __init__(self):
        self.counts = {}
        self.current_counts = {}
        self.prev_indices = None

    def update(self, indices):
        '''Updates counts based on indices. The algorithm tracks the index change at i and
        update global counts for all indices beyond i with local counts tracked so far.
        '''
        if self.prev_indices is None:
            self.prev_indices = indices[:]
            for i in range(len(indices)):
                if i not in self.counts:
                    self.counts[i] = []
                if i not in self.current_counts:
                    self.current_counts[i] = 0
            return
        
        # Find the first level where indices changed
        change_level = None
        for i in range(len(indices)):
            if i >= len(self.prev_indices) or indices[i] != self.prev_indices[i]:
                change_level = i
                break
        
        if change_level is not None:
            # Update counts for all levels beyond the change level
            for level in range(change_level + 1, len(indices)):
                if level in self.current_counts and self.current_counts[level] > 0:
                    if level not in self.counts:
                        self.counts[level] = []
                    self.counts[level].append(self.current_counts[level])
                    self.current_counts[level] = 0
        
        # Update current counts
        for i in range(len(indices)):
            if i not in self.current_counts:
                self.current_counts[i] = 0
            if i not in self.counts:
                self.counts[i] = []
        
        # Increment the deepest level
        if len(indices) > 0:
            deepest_level = len(indices) - 1
            self.current_counts[deepest_level] += 1
        
        self.prev_indices = indices[:]

    def finalize(self):
        '''This will add the very last document to counts. We also get rid of counts[0] since that
        represents document level which doesnt come under anything else. We also convert all count
        values to numpy arrays so that stats can be computed easily.
        '''
        # Add remaining current counts to final counts
        for level in self.current_counts:
            if self.current_counts[level] > 0:
                if level not in self.counts:
                    self.counts[level] = []
                self.counts[level].append(self.current_counts[level])
        
        # Remove document level (level 0) if it exists
        if 0 in self.counts:
            del self.counts[0]
        
        # Convert all count lists to numpy arrays
        for level in self.counts:
            self.counts[level] = np.array(self.counts[level])