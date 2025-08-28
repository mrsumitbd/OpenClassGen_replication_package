class Right:
    '''right'''

    class Result1:
        '''result one'''
        pass

    def work(self) -> 'Right.Result1':
        '''good type hint'''
        return Right.Result1()