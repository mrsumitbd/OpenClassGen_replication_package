class InteractiveQuery:
    '''
    A query (set of prompts) for a user during interactive authentication.
    '''

    def __init__(self, name="", instructions="", *prompts):
        '''
        Create a new interactive query to send to the client.  The name and
        instructions are optional, but are generally displayed to the end
        user.  A list of prompts may be included, or they may be added via
        the `add_prompt` method.

        :param str name: name of this query
        :param str instructions:
            user instructions (usually short) about this query
        :param str prompts: one or more authentication prompts
        '''
        self.name = name
        self.instructions = instructions
        self.prompts = []  # list of dicts: {'prompt': str, 'echo': bool}

        for p in prompts:
            self.add_prompt(p, echo=True)

    def add_prompt(self, prompt, echo=True):
        '''
        Add a prompt to this query.  The prompt should be a (reasonably short)
        string.  Multiple prompts can be added to the same query.

        :param str prompt: the user prompt
        :param bool echo:
            ``True`` (default) if the user's response should be echoed;
            ``False`` if not (for a password or similar)
        '''
        if not isinstance(prompt, str):
            raise TypeError("prompt must be a string")
        if not isinstance(echo, bool):
            raise TypeError("echo flag must be a boolean")

        self.prompts.append({
            'prompt': prompt,
            'echo': echo
        })