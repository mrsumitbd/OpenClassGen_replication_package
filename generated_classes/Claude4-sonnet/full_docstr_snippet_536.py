class Herald(object):
    '''
    Herald's service
    '''

    def __init__(self):
        '''
        '''
        self._peers = {}
        self._links = {}

    def _get_link(self, peer):
        '''
        Returns a link to the given peer

        :return: A Link object
        :raise ValueError: Unknown peer
        '''
        if peer not in self._peers:
            raise ValueError(f"Unknown peer: {peer}")
        
        if peer not in self._links:
            raise ValueError(f"No link to peer: {peer}")
        
        return self._links[peer]

    def send(self, peer_id, message):
        '''
        Synchronously sends a message

        :param peer_id: UUID of a peer
        :param message: Message to send to the peer
        :raise KeyError: Unknown peer
        :raise ValueError: No link to the peer
        '''
        if peer_id not in self._peers:
            raise KeyError(f"Unknown peer: {peer_id}")
        
        link = self._get_link(peer_id)
        return link.send_sync(message)

    def post(self, peer_id, message):
        '''
        Sends a message and returns a Future object to get its result later

        :param peer_id: UUID of a peer
        :param message: Message to send to the peer
        :return: A Future object to grab the response(s) to the message
        :raise KeyError: Unknown peer
        :raise ValueError: No link to the peer
        '''
        if peer_id not in self._peers:
            raise KeyError(f"Unknown peer: {peer_id}")
        
        link = self._get_link(peer_id)
        return link.send_async(message)