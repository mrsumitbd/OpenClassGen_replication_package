class BasicUserInfoHandler(object):
    '''
    Basic OpenID Connect User Info claims.

    For reference see:
    http://openid.net/specs/openid-connect-basic-1_0.html#UserInfo

    '''

    def scope_openid(self, data):
        '''Returns claims for the `openid` profile'''
        return {'sub': self.claim_sub(data)}

    def claim_sub(self, data):
        ''' Required subject identifier. '''
        if 'sub' not in data:
            raise ValueError('Missing required claim "sub"')
        return data['sub']