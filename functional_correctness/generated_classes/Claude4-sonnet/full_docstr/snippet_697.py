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
        self.data = {}
        self.seismicity_rate = None
        self.target_magnitudes = None
        self.data_variables = ['longitude', 'latitude', 'exx', 'eyy', 'exy']

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
        if strain_data is not None:
            self.data = strain_data
        
        exx = np.array(self.data['exx'])
        eyy = np.array(self.data['eyy'])
        exy = np.array(self.data['exy'])
        
        # 2nd invariant of strain
        self.data['e2nd'] = np.sqrt(((exx - eyy) ** 2 + 4 * exy ** 2) / 2)
        
        # Dilatation rate
        self.data['dilatation'] = exx + eyy
        
        # Principal strain rates e1h and e2h
        mean_strain = (exx + eyy) / 2
        diff_strain = np.sqrt(((exx - eyy) / 2) ** 2 + exy ** 2)
        
        self.data['e1h'] = mean_strain + diff_strain
        self.data['e2h'] = mean_strain - diff_strain
        
        # err (radial strain component)
        self.data['err'] = (exx + eyy) / 2
        
        # Update data_variables list
        secondary_vars = ['e2nd', 'dilatation', 'e1h', 'e2h', 'err']
        for var in secondary_vars:
            if var not in self.data_variables:
                self.data_variables.append(var)

    def get_number_observations(self):
        '''
        Returns the number of observations in the data file
        '''
        if not self.data:
            return 0
        
        # Get the length of any data array (they should all be the same length)
        for key, value in self.data.items():
            if isinstance(value, (list, np.ndarray)):
                return len(value)
        
        return 0