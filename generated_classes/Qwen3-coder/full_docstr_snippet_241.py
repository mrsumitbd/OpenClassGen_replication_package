class nl_msg(object):
    '''https://github.com/thom311/libnl/blob/libnl3_2_25/include/netlink-private/types.h#L133.

    Client-side only. Never transmitted to the kernel.

    Instance variables:
    nm_protocol -- integer.
    nm_flags -- integer.
    nm_src -- sockaddr_nl class instance.
    nm_dst -- sockaddr_nl class instance.
    nm_creds -- ucred class instance.
    nm_nlh -- nlmsghdr class instance.
    nm_size -- integer.
    nm_refcnt -- integer.
    '''

    def __init__(self):
        '''Constructor.'''
        self.nm_protocol = 0
        self.nm_flags = 0
        self.nm_src = None
        self.nm_dst = None
        self.nm_creds = None
        self.nm_nlh = None
        self.nm_size = 0
        self.nm_refcnt = 0

    def __repr__(self):
        '''repr() handler.'''
        return f"<nl_msg protocol={self.nm_protocol} flags={self.nm_flags} size={self.nm_size} refcnt={self.nm_refcnt}>"