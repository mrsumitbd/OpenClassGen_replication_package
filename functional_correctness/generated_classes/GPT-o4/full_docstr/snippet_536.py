class Herald(object):
    '''
    Herald's service
    '''

    def __init__(self):
        self._links = {}
        self._executor = ThreadPoolExecutor()

    def _get_link(self, peer):
        '''
        Returns a link to the given peer

        :return: A Link object
        :raise ValueError: Unknown peer
        '''
        if peer not in self._links:
            raise ValueError(f"Unknown peer: {peer}")
        return self._links[peer]

    def send(self, peer_id, message):
        '''
        Synchronously sends a message

        :param peer_id: UUID of a peer
        :param message: Message to send to the peer
        :raise KeyError: Unknown peer
        :raise ValueError: No link to the peer
        '''
        if peer_id not in self._links:
            raise KeyError(f"Unknown peer: {peer_id}")
        link = self._get_link(peer_id)
        if link is None:
            raise ValueError(f"No link to the peer: {peer_id}")
        return link.send(message)

    def post(self, peer_id, message):
        '''
        Sends a message and returns a Future object to get its result later

        :param peer_id: UUID of a peer
        :param message: Message to send to the peer
        :return: A Future object to grab the response(s) to the message
        :raise KeyError: Unknown peer
        :raise ValueError: No link to the peer
        '''
        if peer_id not in self._links:
            raise KeyError(f"Unknown peer: {peer_id}")
        link = self._get_link(peer_id)
        if link is None:
            raise ValueError(f"No link to the peer: {peer_id}")
        return self._executor.submit(link.send, message)