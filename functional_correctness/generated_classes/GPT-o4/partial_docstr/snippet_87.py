class BaseQuery(object):

    @staticmethod
    def normalize_wait(wait):
        """
        Returns the number of seconds to wait.

        Args:
            wait (int | float | bool, optional): The desired wait time in seconds, or ``False`` to
                disable waiting. Defaults to :data:`capybara.default_max_wait_time`.

        Returns:
            int: The number of seconds to wait.
        """
        if wait is False:
            return 0

        if wait is None or wait is True:
            return default_max_wait_time

        if not isinstance(wait, (int, float)):
            raise TypeError("wait must be an int, float, bool or None")

        if wait < 0:
            raise ValueError("wait time must be non-negative")

        return int(wait)