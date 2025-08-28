class _PhaseManager(object):
    ''' Manages iteration cycle phase drivers
  '''

    def __init__(self, model, phaseSpecs):
        '''
        model:   Model instance
        phaseSpecs:   Iteration period description consisting of a sequence of
                      IterationPhaseSpecXXXXX elements that are performed in the
                      given order
        '''
        self.model = model
        self.phaseSpecs = phaseSpecs
        self.currentPhaseIndex = 0
        self.currentPhase = phaseSpecs[0] if phaseSpecs else None

    def __repr__(self):
        return f"_PhaseManager(currentPhaseIndex={self.currentPhaseIndex}, " \
               f"totalPhases={len(self.phaseSpecs)})"

    def __advancePhase(self):
        ''' Advance to the next iteration cycle phase
        '''
        self.currentPhaseIndex += 1
        if self.currentPhaseIndex < len(self.phaseSpecs):
            self.currentPhase = self.phaseSpecs[self.currentPhaseIndex]
        else:
            self.currentPhase = None

    def handleInputRecord(self, inputRecord):
        ''' Processes the given record according to the current phase

        inputRecord:  record object formatted according to
                      nupic.data.FileSource.getNext() result format.

        Returns:      An opf_utils.ModelResult object with the inputs and inferences
                      after the current record is processed by the model
        '''
        if self.currentPhase is None:
            return None
            
        result = self.currentPhase.processRecord(self.model, inputRecord)
        
        # Check if current phase is complete and advance if needed
        if self.currentPhase.isComplete():
            self.__advancePhase()
            
        return result