class EdgeNgramIndexer:

    @staticmethod
    def index(pipe, key, doc, tokens, **kwargs):
        min_gram = kwargs.get('min_gram', 1)
        max_gram = kwargs.get('max_gram', 3)
        
        for token in tokens:
            # Generate edge n-grams (prefixes and suffixes)
            for i in range(min_gram, min(max_gram + 1, len(token) + 1)):
                # Prefix n-grams
                prefix = token[:i]
                pipe.sadd(f"{key}:edge_ngram:{prefix}", doc)
                
                # Suffix n-grams
                suffix = token[-i:]
                pipe.sadd(f"{key}:edge_ngram:{suffix}", doc)

    @staticmethod
    def deindex(db, key, doc, tokens, **kwargs):
        min_gram = kwargs.get('min_gram', 1)
        max_gram = kwargs.get('max_gram', 3)
        
        for token in tokens:
            # Remove edge n-grams (prefixes and suffixes)
            for i in range(min_gram, min(max_gram + 1, len(token) + 1)):
                # Prefix n-grams
                prefix = token[:i]
                db.srem(f"{key}:edge_ngram:{prefix}", doc)
                
                # Suffix n-grams
                suffix = token[-i:]
                db.srem(f"{key}:edge_ngram:{suffix}", doc)