class IApi:
    '''Interface to an Api implementation'''

    def shutdown(self):
        '''Override to perform any shutdown necessary'''
        pass

    def call(self, method, data=None, **args):
        '''
        Generic interface to REST api
        :param method:  query name
        :param data:   dictionary of inputs
        :param args:    keyword arguments added to the payload
        :return:
        '''
        pass

    def on_ws_connect(self):
        '''
        Called by the websocket mixin
        '''
        pass