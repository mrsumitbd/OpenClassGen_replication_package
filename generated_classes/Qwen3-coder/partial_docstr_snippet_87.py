class BaseQuery(object):
    @staticmethod
    def normalize_wait(wait):
        '''
        Returns the number of seconds to wait.

        Args:
            wait (int | float | bool, optional): The desired wait time in seconds, or ``False`` to
                disable waiting. Defaults to :data:`capybara.default_max_wait_time`.

        Returns:
            int: The number of seconds to wait.
        '''
        import capybara
        if wait is False:
            return 0
        elif wait is True:
            return int(capybara.default_max_wait_time)
        elif wait is None:
            return int(capybara.default_max_wait_time)
        else:
            return int(wait)