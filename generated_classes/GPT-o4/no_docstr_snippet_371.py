class TryExcept(object):
    def __init__(self, try_, except_):
        self.try_ = try_
        self.except_ = except_

    def generate(self):
        def _lines(block):
            if hasattr(block, 'generate'):
                code = block.generate()
            else:
                code = block
            if isinstance(code, str):
                return code.splitlines()
            if isinstance(code, list):
                result = []
                for part in code:
                    if hasattr(part, 'generate'):
                        sub = part.generate()
                    else:
                        sub = part
                    if isinstance(sub, str):
                        result.extend(sub.splitlines())
                    elif isinstance(sub, list):
                        result.extend(sub)
                    else:
                        result.extend(str(sub).splitlines())
                return result
            return str(code).splitlines()

        try_lines = _lines(self.try_)
        except_lines = _lines(self.except_)

        out = ["try:"]
        out += ["    " + line for line in try_lines]
        out.append("except:")
        out += ["    " + line for line in except_lines]
        return "\n".join(out)