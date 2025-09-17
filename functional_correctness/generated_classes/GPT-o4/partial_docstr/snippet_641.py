class _PhaseManager(object):
    ''' Manages iteration cycle phase drivers
    '''

    def __init__(self, model, phaseSpecs):
        '''
        model:     Model instance
        phaseSpecs: Sequence of IterationPhaseSpecXXXXX elements
                    that are performed in the given order
        '''
        self.model = model
        self.phaseSpecs = list(phaseSpecs)
        self._numPhases = len(self.phaseSpecs)
        self._phaseIndex = 0
        self._recordsInPhase = 0

        # call onStart of first phase if provided
        first_spec = self.phaseSpecs[0] if self._numPhases > 0 else None
        if first_spec is not None:
            if hasattr(first_spec, "onStart"):
                first_spec.onStart(self.model)
            elif hasattr(first_spec, "start"):
                first_spec.start(self.model)

    def __repr__(self):
        return "<_PhaseManager phase={}/{} recordsInPhase={}>".format(
            self._phaseIndex + 1,
            self._numPhases,
            self._recordsInPhase
        )

    def __advancePhase(self):
        ''' Advance to the next iteration cycle phase '''
        if self._numPhases == 0:
            return

        # finish current phase
        cur = self.phaseSpecs[self._phaseIndex]
        if hasattr(cur, "onFinish"):
            cur.onFinish(self.model)
        elif hasattr(cur, "finish"):
            cur.finish(self.model)

        # advance index
        self._phaseIndex = (self._phaseIndex + 1) % self._numPhases
        self._recordsInPhase = 0

        # start next phase
        nxt = self.phaseSpecs[self._phaseIndex]
        if hasattr(nxt, "onStart"):
            nxt.onStart(self.model)
        elif hasattr(nxt, "start"):
            nxt.start(self.model)

    def handleInputRecord(self, inputRecord):
        ''' Processes the given record according to the current phase

        inputRecord:  record object formatted according to
                      nupic.data.FileSource.getNext() result format.

        Returns:      An opf_utils.ModelResult object
                      after processing this record
        '''
        if self._numPhases == 0:
            # no phases; just run the model
            if hasattr(self.model, "run"):
                return self.model.run(inputRecord)
            elif hasattr(self.model, "runRecord"):
                return self.model.runRecord(inputRecord)
            else:
                raise RuntimeError("Model has no run method")

        spec = self.phaseSpecs[self._phaseIndex]

        # process the record via spec or directly via model
        if hasattr(spec, "processRecord"):
            result = spec.processRecord(self.model, inputRecord)
        elif hasattr(spec, "runRecord"):
            result = spec.runRecord(self.model, inputRecord)
        else:
            # fallback to model
            if hasattr(self.model, "run"):
                result = self.model.run(inputRecord)
            elif hasattr(self.model, "runRecord"):
                result = self.model.runRecord(inputRecord)
            else:
                raise RuntimeError("Neither spec nor model can run inputRecord")

        # update counter
        self._recordsInPhase += 1

        # check for phase completion
        done = False
        # by explicit length
        if hasattr(spec, "length"):
            done = self._recordsInPhase >= spec.length
        elif hasattr(spec, "period"):
            done = self._recordsInPhase >= spec.period
        elif hasattr(spec, "isComplete"):
            try:
                done = spec.isComplete(self._recordsInPhase)
            except TypeError:
                done = spec.isComplete()

        if done:
            self.__advancePhase()

        return result