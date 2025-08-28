class HelpMsgMixIn(object):
    ''' A helper class providing the ability to store a help message in the class or in the instance, and to get a
    formatted help message '''

    def get_help_msg(self):
        '''
        The method used to get the formatted help message according to kwargs. By default it returns the 'help_msg'
        attribute, whether it is defined at the instance level or at the class level.

        The help message is formatted according to help_msg.format(**context),
        where `context = self.get_context_for_help_msgs()` so that subclasses may easily override the behaviour.

        :return: the formatted help message
        '''
        help_msg = getattr(self, 'help_msg', '')
        context = self.get_context_for_help_msgs()
        return help_msg.format(**context)

    def get_context_for_help_msgs(self):
        ''' Subclasses may wish to override this method to change the dictionary of contextual information before it is
        sent to the help message formatter '''
        return {}