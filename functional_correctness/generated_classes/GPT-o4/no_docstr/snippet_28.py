class EdgeNgramIndexer:

    @staticmethod
    def index(pipe, key, doc, tokens, min_gram=1, max_gram=20):
        """
        For each token, generate edge n-grams of lengths from min_gram up to max_gram (or token length)
        and add the document ID to the corresponding Redis set.
        """
        for token in tokens:
            token_length = len(token)
            upper = min(max_gram, token_length)
            for n in range(min_gram, upper + 1):
                ngram = token[:n]
                set_key = f"{key}:{ngram}"
                pipe.sadd(set_key, doc)

    @staticmethod
    def deindex(db, key, doc, tokens, min_gram=1, max_gram=20):
        """
        Remove the document ID from all edge n-gram sets for the given tokens.
        If after removal a set is empty, delete the key from Redis.
        """
        for token in tokens:
            token_length = len(token)
            upper = min(max_gram, token_length)
            for n in range(min_gram, upper + 1):
                ngram = token[:n]
                set_key = f"{key}:{ngram}"
                db.srem(set_key, doc)
                if db.scard(set_key) == 0:
                    db.delete(set_key)