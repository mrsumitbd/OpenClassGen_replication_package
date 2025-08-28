class nl_msgtype(object):
    '''Message type to cache action association.

    https://github.com/thom311/libnl/blob/libnl3_2_25/include/netlink-private/cache-api.h#L117

    Positional arguments:
    mt_id -- Netlink message type (c_int).
    mt_act -- cache action to take (c_int).
    mt_name -- name of operation for human-readable printing (string).
    '''

    def __init__(self, mt_id, mt_act, mt_name):
        '''Constructor.'''
        self.mt_id = mt_id
        self.mt_act = mt_act
        self.mt_name = mt_name

    def __repr__(self):
        '''repr() handler.'''
        return f"nl_msgtype(mt_id={self.mt_id}, mt_act={self.mt_act}, mt_name='{self.mt_name}')"