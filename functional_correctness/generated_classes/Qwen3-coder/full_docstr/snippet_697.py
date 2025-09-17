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

    def __init__(self):
        '''Instantiates'''
        self.data = None
        self.seismicity_rate = None
        self.target_magnitudes = None
        self.data_variables = None

    def get_secondary_strain_data(self, strain_data=None):
        '''
        Calculate the following and add to data dictionary:
        1) 2nd invariant of strain
        2) Dilatation rate
        3) e1h and e2h
        4) err

        :param dict strain_data:
            Strain data dictionary (as described) - will overwrite current
            data if input

        '''
        if strain_data is not None:
            self.data = strain_data
        
        if self.data is None:
            raise ValueError("No strain data available")
        
        # Extract strain components
        exx = self.data['exx']
        eyy = self.data['eyy']
        exy = self.data['exy']
        
        # 1) Second invariant of strain: sqrt(exx^2 + eyy^2 + 2*exy^2)
        second_invariant = np.sqrt(exx**2 + eyy**2 + 2.0 * exy**2)
        self.data['second_invariant'] = second_invariant
        
        # 2) Dilatation rate: exx + eyy
        dilatation = exx + eyy
        self.data['dilatation'] = dilatation
        
        # 3) Principal strains e1h and e2h
        # e1h = (exx + eyy)/2 + sqrt(((exx - eyy)/2)^2 + exy^2)
        # e2h = (exx + eyy)/2 - sqrt(((exx - eyy)/2)^2 + exy^2)
        mean_strain = (exx + eyy) / 2.0
        strain_diff = (exx - eyy) / 2.0
        shear_magnitude = np.sqrt(strain_diff**2 + exy**2)
        
        e1h = mean_strain + shear_magnitude
        e2h = mean_strain - shear_magnitude
        
        self.data['e1h'] = e1h
        self.data['e2h'] = e2h
        
        # 4) Maximum shear strain: err = (e1h - e2h) / 2
        err = (e1h - e2h) / 2.0
        self.data['err'] = err

    def get_number_observations(self):
        '''
        Returns the number of observations in the data file
        '''
        if self.data is None:
            return 0
        # Assuming all data arrays have the same length
        for key in self.data:
            return len(self.data[key])
        return 0