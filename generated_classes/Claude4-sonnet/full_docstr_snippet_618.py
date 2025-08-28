class BasicUserInfoHandler(object):
    '''
    Basic OpenID Connect User Info claims.

    For reference see:
    http://openid.net/specs/openid-connect-basic-1_0.html#UserInfo

    '''

    def scope_openid(self, data):
        '''Returns claims for the `openid` profile'''
        return {
            'sub': self.claim_sub(data)
        }

    def claim_sub(self, data):
        ''' Required subject identifier. '''
        if hasattr(data, 'id'):
            return str(data.id)
        elif hasattr(data, 'pk'):
            return str(data.pk)
        elif isinstance(data, dict) and 'id' in data:
            return str(data['id'])
        elif isinstance(data, dict) and 'sub' in data:
            return str(data['sub'])
        else:
            return str(data)