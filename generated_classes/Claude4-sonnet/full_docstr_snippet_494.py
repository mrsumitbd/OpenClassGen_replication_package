class Ngram(object):
    '''
    N-gram
    '''

    def generate_ngram_data_set(self, token_list, n=2):
        '''
        Generate the N-gram's pair.

        Args:
            token_list:     The list of tokens.
            n               N

        Returns:
            zip of Tuple(Training N-gram data, Target N-gram data)
        '''
        if len(token_list) < n + 1:
            return zip([], [])
        
        training_data = []
        target_data = []
        
        for i in range(len(token_list) - n):
            training_data.append(tuple(token_list[i:i+n]))
            target_data.append(token_list[i+n])
        
        return zip(training_data, target_data)

    def generate_skip_gram_data_set(self, token_list):
        '''
        Generate the Skip-gram's pair.

        Args:
            token_list:     The list of tokens.

        Returns:
            zip of Tuple(Training N-gram data, Target N-gram data)
        '''
        if len(token_list) < 3:
            return zip([], [])
        
        training_data = []
        target_data = []
        
        for i in range(1, len(token_list) - 1):
            training_data.append(token_list[i])
            target_data.append(token_list[i-1])
            training_data.append(token_list[i])
            target_data.append(token_list[i+1])
        
        return zip(training_data, target_data)

    def generate_tuple_zip(self, token_list, n=2):
        '''
        Generate the N-gram.

        Args:
            token_list:     The list of tokens.
            n               N

        Returns:
            zip of Tuple(N-gram)
        '''
        if len(token_list) < n:
            return zip([])
        
        ngrams = []
        for i in range(len(token_list) - n + 1):
            ngrams.append(tuple(token_list[i:i+n]))
        
        return zip(ngrams)