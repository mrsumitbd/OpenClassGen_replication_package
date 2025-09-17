class Pushover(object):
    '''Pushover client

    args
    api_token -- pushover API token (https://pushover.net/apps)
    user -- pushover user key (https://pushover.net/)
    '''

    def __init__(self, api_token, user):
        self.api_token = api_token
        self.user = user
        self.base_url = "https://api.pushover.net/1"

    def validate(self):
        '''Validate the user and token, returns the Requests response.'''
        url = f"{self.base_url}/users/validate.json"
        data = {
            'token': self.api_token,
            'user': self.user
        }
        return requests.post(url, data=data)

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
        url = f"{self.base_url}/messages.json"
        data = {
            'token': self.api_token,
            'user': self.user,
            'message': message
        }
        
        if device is not None:
            data['device'] = device
        if title is not None:
            data['title'] = title
        if url is not None:
            data['url'] = url
        if url_title is not None:
            data['url_title'] = url_title
        if priority is not None:
            data['priority'] = priority
        if timestamp is not None:
            data['timestamp'] = timestamp
        if sound is not None:
            data['sound'] = sound
            
        return requests.post(url, data=data)