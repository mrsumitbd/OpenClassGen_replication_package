class DefiniteClause:
    def __init__(self, text):
        self.original_text = text.strip()
        self.head = None
        self.body = []
        self.__parse(text)

    def __parse(self, text):
        text = text.strip()
        if text.endswith('.'):
            text = text[:-1]
        
        if ':-' in text:
            parts = text.split(':-', 1)
            self.head = parts[0].strip()
            body_text = parts[1].strip()
            if body_text:
                self.body = [term.strip() for term in body_text.split(',')]
        else:
            self.head = text
            self.body = []

    def standardize(self, var="x"):
        var_counter = 0
        var_mapping = {}
        
        def replace_vars(term):
            nonlocal var_counter
            pattern = r'\b[A-Z][a-zA-Z0-9_]*\b'
            
            def replace_match(match):
                nonlocal var_counter
                old_var = match.group(0)
                if old_var not in var_mapping:
                    var_mapping[old_var] = f"{var}{var_counter}"
                    var_counter += 1
                return var_mapping[old_var]
            
            return re.sub(pattern, replace_match, term)
        
        new_head = replace_vars(self.head) if self.head else None
        new_body = [replace_vars(term) for term in self.body]
        
        standardized_clause = DefiniteClause("")
        standardized_clause.head = new_head
        standardized_clause.body = new_body
        
        return standardized_clause

    def __str__(self):
        if not self.body:
            return f"{self.head}."
        else:
            body_str = ", ".join(self.body)
            return f"{self.head} :- {body_str}."