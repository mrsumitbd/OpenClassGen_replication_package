class Holidays(object):
    def __init__(self, rules=None):
        self.rules = rules or []

    def month_length(self, year, month):
        return calendar.monthrange(year, month)[1]

    def _day_rule_matches(self, rule, dt):
        if rule.get('month') and rule['month'] != dt.month:
            return False
        if rule.get('day') and rule['day'] != dt.day:
            return False
        if rule.get('year') and rule['year'] != dt.year:
            return False
        return True

    def _weekday_rule_matches(self, rule, dt):
        if rule.get('month') and rule['month'] != dt.month:
            return False
        if rule.get('weekday') is not None and rule['weekday'] != dt.weekday():
            return False
        if rule.get('week'):
            # Calculate which week of the month this is
            first_day = dt.replace(day=1)
            week_num = ((dt.day - 1) // 7) + 1
            if rule['week'] < 0:
                # Negative week means counting from end of month
                last_day = self.month_length(dt.year, dt.month)
                days_from_end = last_day - dt.day
                week_from_end = (days_from_end // 7) + 1
                if week_from_end != abs(rule['week']):
                    return False
            else:
                if week_num != rule['week']:
                    return False
        return True

    def isholiday(self, dt):
        if isinstance(dt, str):
            dt = datetime.strptime(dt, '%Y-%m-%d').date()
        elif isinstance(dt, datetime):
            dt = dt.date()
        
        for rule in self.rules:
            if rule.get('type') == 'day' or 'day' in rule:
                if self._day_rule_matches(rule, dt):
                    return True
            elif rule.get('type') == 'weekday' or 'weekday' in rule:
                if self._weekday_rule_matches(rule, dt):
                    return True
        return False

    def __call__(self, curr, end=None):
        if isinstance(curr, str):
            curr = datetime.strptime(curr, '%Y-%m-%d').date()
        elif isinstance(curr, datetime):
            curr = curr.date()
            
        if end is None:
            return self.isholiday(curr)
        
        if isinstance(end, str):
            end = datetime.strptime(end, '%Y-%m-%d').date()
        elif isinstance(end, datetime):
            end = end.date()
        
        holidays = []
        current = curr
        while current <= end:
            if self.isholiday(current):
                holidays.append(current)
            current += timedelta(days=1)
        return holidays