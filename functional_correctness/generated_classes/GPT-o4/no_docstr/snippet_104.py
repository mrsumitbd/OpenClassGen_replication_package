class DefiniteClause:
    def __init__(self, text):
        self.text = text.strip()
        self.head, self.body = self.__parse(self.text)

    def __parse(self, text):
        t = text.strip()
        if t.endswith('.'):
            t = t[:-1].strip()
        if ':-' in t:
            head_str, body_str = t.split(':-', 1)
            body_preds = [p.strip() for p in body_str.split(',')]
        else:
            head_str = t
            body_preds = []
        def parse_pred(p):
            if '(' in p and p.endswith(')'):
                name = p[:p.index('(')].strip()
                args_str = p[p.index('(')+1:-1]
                args = [arg.strip() for arg in args_str.split(',') if arg.strip()]
            else:
                name = p.strip()
                args = []
            return (name, args)
        head = parse_pred(head_str.strip())
        body = [parse_pred(p) for p in body_preds]
        return head, body

    def standardize(self, var="x"):
        mapping = {}
        counter = [1]
        def rename_term(arg):
            if arg and arg[0].isupper():
                if arg not in mapping:
                    mapping[arg] = f"{var}{counter[0]}"
                    counter[0] += 1
                return mapping[arg]
            return arg
        new_head = (self.head[0], [rename_term(a) for a in self.head[1]])
        new_body = []
        for name, args in self.body:
            new_body.append((name, [rename_term(a) for a in args]))
        def pred_to_str(pred):
            name, args = pred
            if args:
                return f"{name}({', '.join(args)})"
            return name
        head_str = pred_to_str(new_head)
        if new_body:
            body_strs = [pred_to_str(p) for p in new_body]
            clause_str = f"{head_str} :- {', '.join(body_strs)}."
        else:
            clause_str = f"{head_str}."
        return DefiniteClause(clause_str)

    def __str__(self):
        def pred_to_str(pred):
            name, args = pred
            if args:
                return f"{name}({', '.join(args)})"
            return name
        head_str = pred_to_str(self.head)
        if self.body:
            body_strs = [pred_to_str(p) for p in self.body]
            return f"{head_str} :- {', '.join(body_strs)}."
        return f"{head_str}."