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
        return (f"nl_msg(nm_protocol={self.nm_protocol}, nm_flags={self.nm_flags}, "
                f"nm_src={self.nm_src}, nm_dst={self.nm_dst}, nm_creds={self.nm_creds}, "
                f"nm_nlh={self.nm_nlh}, nm_size={self.nm_size}, nm_refcnt={self.nm_refcnt})")