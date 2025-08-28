class GGData(object):

    def __init__(self, r_commands, fname=None):
        if not isinstance(r_commands, (list, tuple)):
            raise TypeError("r_commands must be a list or tuple")
        self.r_commands = [str(cmd) for cmd in r_commands]
        self.fname = fname
        if self.fname:
            with open(self.fname, "w") as f:
                f.write("\n".join(self.r_commands))

    def __str__(self):
        return "\n".join(self.r_commands)