class GeodeticStrain(object):
    '''
    :class:`openquake.hmtk.strain.geodetic_strain.GeodeticStrain` describes
    the geodetic strain model

    :param dict data:
        Strain data in the form of a dictionary where is vector of attributes
        is stored under the correponding dictionary key (i.e.
        - longitude - Longitude of point
        - latitude - Latitiude of point
        - exx - xx-component of strain tensor
        - eyy - yy-component of strain tensor
        - exy - xy-component of strain tensor
    :param numpy.ndarray seismicity_rate:
        Seismicity rate at each point associated with the strain model
    :param numpy.ndarray target_magnitudes:
        Magnitudes for the corresponding activity rates
    :param list data_variables:
        List of strain data attributes in the current class
    '''

    def __init__(self, data, seismicity_rate, target_magnitudes, data_variables):
        self.data = data
        self.seismicity_rate = np.asarray(seismicity_rate)
        self.target_magnitudes = np.asarray(target_magnitudes)
        self.data_variables = list(data_variables)

    def get_secondary_strain_data(self, strain_data=None):
        '''
        Calculate the following and add to data dictionary:
        1) 2nd invarient of strain
        2) Dilatation rate
        3) e1h and e2h
        4) err

        :param dict strain_data:
            Strain data dictionary (as described) - will overwrite current
            data if input
        '''
        dd = strain_data if strain_data is not None else self.data

        exx = np.asarray(dd['exx'])
        eyy = np.asarray(dd['eyy'])
        exy = np.asarray(dd['exy'])

        # Dilatation rate
        dilatation = exx + eyy

        # Principal strains
        mean = 0.5 * (exx + eyy)
        diff = 0.5 * (exx - eyy)
        root = np.sqrt(diff**2 + exy**2)
        e1h = mean + root
        e2h = mean - root

        # Second invariant of deviatoric strain (J2)
        # here taken as the magnitude of the deviatoric part: root
        invariant_2nd = root

        # Principal axis orientation
        err = 0.5 * np.arctan2(2 * exy, exx - eyy)

        # Store
        dd['dilatation'] = dilatation
        dd['e1h'] = e1h
        dd['e2h'] = e2h
        dd['invariant_2nd'] = invariant_2nd
        dd['err'] = err

        for key in ['dilatation', 'e1h', 'e2h', 'invariant_2nd', 'err']:
            if key not in self.data_variables:
                self.data_variables.append(key)

        if strain_data is None:
            self.data = dd

        return dd

    def get_number_observations(self):
        '''
        Returns the number of observations in the data file
        '''
        # assume all variables are same length
        first_key = next(iter(self.data))
        return len(self.data[first_key])