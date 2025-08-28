class DefiniteClause:
    def __init__(self, text):
        self.head, self.body = self.__parse(text)
    
    def __parse(self, text):
        if ":-" in text:
            head, body_text = text.split(":-")
            head = head.strip()
            body_literals = [lit.strip() for lit in body_text.strip().rstrip('.').split(',')]
            return head, body_literals
        else:
            head = text.strip().rstrip('.')
            return head, []
    
    def standardize(self, var="x"):
        # Replace all variables (assumed to be single lowercase letters) with the given variable
        def replace_vars(term):
            result = ""
            i = 0
            while i < len(term):
                if term[i].islower() and (i == 0 or not term[i-1].isalpha()) and (i == len(term)-1 or not term[i+1].isalpha()):
                    result += var
                else:
                    result += term[i]
                i += 1
            return result
        
        new_head = replace_vars(self.head)
        new_body = [replace_vars(literal) for literal in self.body]
        return DefiniteClause(new_head + " :- " + ", ".join(new_body) + "." if new_body else new_head + ".")
    
    def __str__(self):
        if self.body:
            return self.head + " :- " + ", ".join(self.body) + "."
        else:
            return self.head + "."