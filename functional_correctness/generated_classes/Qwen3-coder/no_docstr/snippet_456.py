class Holidays(object):
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def month_length(self, year, month):
        return calendar.monthrange(year, month)[1]

    def _day_rule_matches(self, rule, dt):
        if rule.get('type') == 'date':
            return (rule.get('month') == dt.month and 
                    rule.get('day') == dt.day)
        return False

    def _weekday_rule_matches(self, rule, dt):
        if rule.get('type') == 'weekday':
            if rule.get('month') != dt.month:
                return False
            weekday = rule.get('weekday')
            week = rule.get('week')
            if week == 'last':
                # Check if it's the last occurrence of this weekday in the month
                days_in_month = self.month_length(dt.year, dt.month)
                last_occurrence = dt.replace(day=days_in_month)
                while last_occurrence.weekday() != weekday:
                    last_occurrence = last_occurrence.replace(day=last_occurrence.day - 1)
                return dt.day == last_occurrence.day
            else:
                # Check if it's the nth occurrence of this weekday in the month
                first_day = dt.replace(day=1)
                first_weekday = first_day.weekday()
                target_weekday_first = (weekday - first_weekday) % 7
                if target_weekday_first == 0:
                    target_weekday_first = 7
                target_date = 1 + target_weekday_first + (week - 1) * 7
                if target_date > self.month_length(dt.year, dt.month):
                    return False
                return dt.day == target_date
        return False

    def isholiday(self, dt):
        for rule in self.rules:
            if (self._day_rule_matches(rule, dt) or 
                self._weekday_rule_matches(rule, dt)):
                return True
        return False

    def __call__(self, curr, end=None):
        if end is None:
            return self.isholiday(curr)
        else:
            result = []
            current = curr
            while current <= end:
                if self.isholiday(current):
                    result.append(current)
                current += datetime.timedelta(days=1)
            return result