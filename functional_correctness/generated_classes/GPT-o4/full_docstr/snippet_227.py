class Right:
    '''right'''

    class Result1:
        '''result one'''
        def __init__(self, result: int) -> None:
            self.result = result

        def __repr__(self) -> str:
            return f'Result1(result={self.result})'

    def __init__(self, value: int) -> None:
        self.value = value

    def work(self) -> Result1:
        '''good type hint'''
        computed = self.value ** 2
        return self.Result1(computed)