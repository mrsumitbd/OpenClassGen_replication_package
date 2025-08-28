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
        # protocol family (e.g. NETLINK_ROUTE)
        self.nm_protocol = 0
        # message flags (e.g. NLM_F_REQUEST)
        self.nm_flags = 0
        # source sockaddr_nl
        self.nm_src = sockaddr_nl()
        # destination sockaddr_nl
        self.nm_dst = sockaddr_nl()
        # credentials ucred
        self.nm_creds = ucred()
        # netlink message header
        self.nm_nlh = nlmsghdr()
        # total message size
        self.nm_size = 0
        # reference count
        self.nm_refcnt = 1

    def __repr__(self):
        '''repr() handler.'''
        cls = self.__class__.__name__
        return (
            f"{cls}(nm_protocol={self.nm_protocol!r}, "
            f"nm_flags={self.nm_flags!r}, "
            f"nm_src={self.nm_src!r}, "
            f"nm_dst={self.nm_dst!r}, "
            f"nm_creds={self.nm_creds!r}, "
            f"nm_nlh={self.nm_nlh!r}, "
            f"nm_size={self.nm_size!r}, "
            f"nm_refcnt={self.nm_refcnt!r})"
        )