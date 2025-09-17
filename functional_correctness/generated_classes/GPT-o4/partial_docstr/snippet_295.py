class Pushover(object):
    '''Pushover client

    args
    api_token -- pushover API token (https://pushover.net/apps)
    user -- pushover user key (https://pushover.net/)
    '''

    VALIDATE_URL = 'https://api.pushover.net/1/users/validate.json'
    MESSAGE_URL = 'https://api.pushover.net/1/messages.json'

    def __init__(self, api_token, user):
        self.api_token = api_token
        self.user = user

    def validate(self):
        '''Validate the user and token, returns the Requests response.'''
        payload = {
            'token': self.api_token,
            'user': self.user,
        }
        return requests.post(self.VALIDATE_URL, data=payload)

    def push(self, message, device=None, title=None, url=None, url_title=None,
             priority=None, timestamp=None, sound=None):
        '''Pushes the notification, returns the Requests response.

        Arguments:
            message -- your message

        Keyword arguments:
            device -- your user's device name to send the message directly to
                that device, rather than all of the user's devices
            title -- your message's title, otherwise your app's name is used
            url -- a supplementary URL to show with your message
            url_title -- a title for your supplementary URL, otherwise just the
                URL is shown
            priority -- send as --1 to always send as a quiet notification, 1
                to display as high--priority and bypass the user's quiet hours,
                or 2 to also require confirmation from the user
            timestamp -- a Unix timestamp of your message's date and time to
                display to the user, rather than the time your message is
                received by our API
            sound -- the name of one of the sounds supported by device clients
                to override the user's default sound choice.
        '''
        payload = {
            'token': self.api_token,
            'user': self.user,
            'message': message,
        }
        if device is not None:
            payload['device'] = device
        if title is not None:
            payload['title'] = title
        if url is not None:
            payload['url'] = url
        if url_title is not None:
            payload['url_title'] = url_title
        if priority is not None:
            payload['priority'] = priority
        if timestamp is not None:
            payload['timestamp'] = timestamp
        if sound is not None:
            payload['sound'] = sound

        return requests.post(self.MESSAGE_URL, data=payload)