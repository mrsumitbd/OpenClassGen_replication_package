class EdgeNgramIndexer:

    @staticmethod
    def index(pipe, key, doc, tokens, **kwargs):
        min_gram = kwargs.get('min_gram', 1)
        max_gram = kwargs.get('max_gram', 3)
        
        for token in tokens:
            token_str = str(token).lower()
            for i in range(min_gram, min(len(token_str) + 1, max_gram + 1)):
                ngram = token_str[:i]
                pipe.sadd(f"{key}:{ngram}", doc)

    @staticmethod
    def deindex(db, key, doc, tokens, **kwargs):
        min_gram = kwargs.get('min_gram', 1)
        max_gram = kwargs.get('max_gram', 3)
        
        for token in tokens:
            token_str = str(token).lower()
            for i in range(min_gram, min(len(token_str) + 1, max_gram + 1)):
                ngram = token_str[:i]
                db.srem(f"{key}:{ngram}", doc)