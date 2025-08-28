class StopProcessing(object):
    '''
    Stop processing rules and actions for the given file
    '''

    def __init__(self, value=None):
        self.value = value

    @staticmethod
    def do_action(target, dry_run=False):
        '''
        :param target: Full path and filename
        :param dry_run: True - don't actually perform action. False: perform action. No effect for this rule.
        :return: None
        '''
        pass