class ICRS(object):
    '''The International Celestial Reference System (ICRS).

    The ICRS is a permanent reference frame which has replaced J2000,
    with which its axes agree to within 0.02 arcseconds (closer than the
    precision of J2000 itself).  The ICRS also supersedes older
    equinox-based systems like B1900 and B1950.

    '''

    @staticmethod
    def rotation_at(t):
        """
        Return the rotation matrix at time t that transforms coordinates
        from the ICRS frame to itself (identity, since ICRS is inertial).
        """
        return np.eye(3)