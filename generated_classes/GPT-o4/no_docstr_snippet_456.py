class Holidays(object):
    def __init__(self, rules=None):
        """
        rules is a list of dicts. Each dict is either:
        {"month": M, "day": D}                    # fixed date holiday
        or
        {"month": M, "weekday": W, "n": N}        # Nth W-day of month, N can be negative
        """
        self.rules = rules or []

    def month_length(self, year, month):
        return calendar.monthrange(year, month)[1]

    def _day_rule_matches(self, rule, dt):
        return dt.month == rule["month"] and dt.day == rule["day"]

    def _weekday_rule_matches(self, rule, dt):
        if dt.month != rule["month"] or dt.weekday() != rule["weekday"]:
            return False
        n = rule["n"]
        # count occurrences of that weekday from start of month to dt
        if n > 0:
            count = 0
            for day in range(1, dt.day + 1):
                if datetime.date(dt.year, dt.month, day).weekday() == rule["weekday"]:
                    count += 1
            return count == n
        # count from end of month backwards
        else:
            count = 0
            last_day = self.month_length(dt.year, dt.month)
            for day in range(last_day, dt.day - 1, -1):
                if datetime.date(dt.year, dt.month, day).weekday() == rule["weekday"]:
                    count -= 1
            return count == n

    def isholiday(self, dt):
        for rule in self.rules:
            if "day" in rule:
                if self._day_rule_matches(rule, dt):
                    return True
            else:
                if self._weekday_rule_matches(rule, dt):
                    return True
        return False

    def __call__(self, curr, end=None):
        if end is None:
            return self.isholiday(curr)
        date = curr
        one_day = datetime.timedelta(days=1)
        while date <= end:
            if self.isholiday(date):
                yield date
            date += one_day