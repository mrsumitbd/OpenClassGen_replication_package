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
        tuples = list(self.generate_tuple_zip(token_list, n))
        X = [t[:-1] for t in tuples]
        y = [t[-1] for t in tuples]
        return zip(X, y)

    def generate_skip_gram_data_set(self, token_list):
        '''
        Generate the Skip-gram's pair.

        Args:
            token_list:     The list of tokens.

        Returns:
            zip of Tuple(Training N-gram data, Target N-gram data)
        '''
        X, y = [], []
        length = len(token_list)
        for i, center in enumerate(token_list):
            for j in (-1, 1):
                ctx_i = i + j
                if 0 <= ctx_i < length:
                    X.append(center)
                    y.append(token_list[ctx_i])
        return zip(X, y)

    def generate_tuple_zip(self, token_list, n=2):
        '''
        Generate the N-gram.

        Args:
            token_list:     The list of tokens.
            n               N

        Returns:
            zip of Tuple(N-gram)
        '''
        if n <= 0:
            return iter(())
        slices = [token_list[i:] for i in range(n)]
        return zip(*slices)