class PanelMetricsHelper:
    def front_to_back(self, name):
        if not name:
            return ''
        # camelCase or PascalCase to snake_case
        s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
        s2 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1)
        return s2.lower()

    def back_to_front(self, name):
        if not name:
            return ''
        parts = name.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

    def special_front_to_back(self, name):
        if not name:
            return ''
        # replace spaces or hyphens with underscores, then camel→snake
        temp = re.sub(r'[\s\-]+', '_', name.strip())
        return self.front_to_back(temp)

    def special_back_to_front(self, name):
        if not name:
            return ''
        # snake or kebab to Title Case with spaces
        temp = re.sub(r'[_\-]+', ' ', name.strip())
        return temp.title()