class GGData(object):

    def __init__(self, r_commands, fname=None):
        self.r_commands = r_commands
        self.fname = fname

    def __str__(self):
        if self.fname:
            return f"GGData(r_commands={self.r_commands}, fname='{self.fname}')"
        else:
            return f"GGData(r_commands={self.r_commands}, fname=None)"