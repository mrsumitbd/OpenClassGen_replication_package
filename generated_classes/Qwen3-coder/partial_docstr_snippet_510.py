class ICRS(object):
    '''The International Celestial Reference System (ICRS).

    The ICRS is a permanent reference frame which has replaced J2000,
    with which its axes agree to within 0.02 arcseconds (closer than the
    precision of J2000 itself).  The ICRS also supersedes older
    equinox-based systems like B1900 and B1950.

    '''

    @staticmethod
    def rotation_at(t):
        '''
        Calculate the rotation matrix from ICRS to equatorial coordinates at a given time.
        
        Parameters
        ----------
        t : astropy.time.Time or compatible
            The time at which to calculate the rotation matrix
            
        Returns
        -------
        numpy.ndarray
            3x3 rotation matrix
        '''
        # For ICRS, the rotation matrix is typically the identity matrix
        # since ICRS is the standard reference frame
        return np.eye(3)