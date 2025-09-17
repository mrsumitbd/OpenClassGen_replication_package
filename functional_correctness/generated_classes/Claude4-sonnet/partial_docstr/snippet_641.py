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
        self._model = model
        self._phaseSpecs = phaseSpecs
        self._currentPhaseIndex = 0
        self._currentPhaseIterationCount = 0
        
        if not phaseSpecs:
            raise ValueError("phaseSpecs cannot be empty")

    def __repr__(self):
        return "PhaseManager(currentPhase=%d, phaseCount=%d, currentIteration=%d)" % (
            self._currentPhaseIndex, 
            len(self._phaseSpecs), 
            self._currentPhaseIterationCount
        )

    def __advancePhase(self):
        ''' Advance to the next iteration cycle phase
        '''
        self._currentPhaseIndex = (self._currentPhaseIndex + 1) % len(self._phaseSpecs)
        self._currentPhaseIterationCount = 0

    def handleInputRecord(self, inputRecord):
        ''' Processes the given record according to the current phase

        inputRecord:  record object formatted according to
                      nupic.data.FileSource.getNext() result format.

        Returns:      An opf_utils.ModelResult object with the inputs and inferences
                      after the current record is processed by the model
        '''
        currentPhase = self._phaseSpecs[self._currentPhaseIndex]
        
        # Process the record based on current phase settings
        if hasattr(currentPhase, 'enableLearning'):
            self._model.enableLearning = currentPhase.enableLearning
        if hasattr(currentPhase, 'enableInference'):
            self._model.enableInference = currentPhase.enableInference
            
        # Run the model on the input record
        result = self._model.run(inputRecord)
        
        # Update iteration count and check if we need to advance phase
        self._currentPhaseIterationCount += 1
        
        if (hasattr(currentPhase, 'iterationCount') and 
            currentPhase.iterationCount is not None and
            self._currentPhaseIterationCount >= currentPhase.iterationCount):
            self.__advancePhase()
            
        return result