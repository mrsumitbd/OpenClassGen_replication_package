class Param(object):
    def __init__(self, name, fmt, types, required, validator, min_bed_fields=None):
        '''
        Parameters
        ----------

        name : str
            Name of the parameter

        fmt : list
            List of strings parsed from the "format" section of the spec from
            UCSC. Mostly used as an informal guide to the format.

        types : list
            List of track types this parameter applies to

        required : bool or list
            If True, all tracks must have it. If list, only those types must
            have it.

        validator : callable, set, or type
            Validation to run on user-provided values. If callable, must return
            True if the value passes. If set, validation will pass if the value
            is in the provided set.

        min_bed_fields : int
            Some parameters only work for a certain number of BED fields.
            Specify that here.

        Examples
        --------

        >>> Param(name='test', fmt=['test <#>'], types=['bigBed'], required=False, validator=int).validate(999)
        True

        >>> Param(name='test', fmt=['test <#>'], types=['bigBed'], required=False, validator=int).validate('999')
        True

        >>> Param(name='test', fmt=['test <#>'], types=['bigBed'], required=False, validator=int).validate(0)
        True
        '''
        self.name = name
        self.fmt = fmt
        self.types = types
        self.required = required
        self.validator = validator
        self.min_bed_fields = min_bed_fields

    def __str__(self):
        return self.name

    def validate(self, value):
        if isinstance(self.validator, type):
            try:
                self.validator(value)
                return True
            except (TypeError, ValueError):
                return False
        elif isinstance(self.validator, set):
            return value in self.validator
        elif callable(self.validator):
            return self.validator(value)
        else:
            return True