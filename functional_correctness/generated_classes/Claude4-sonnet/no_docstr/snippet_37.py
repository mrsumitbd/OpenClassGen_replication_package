class TwoAttributeComparison:
    def __init__(self, leftAttribute, operationString, rightAttribute):
        self.leftAttribute = leftAttribute
        self.operationString = operationString
        self.rightAttribute = rightAttribute

    def getQuery(self, store):
        left_table = self.leftAttribute.split('.')[0]
        right_table = self.rightAttribute.split('.')[0]
        return f"{left_table}.{self.leftAttribute.split('.')[1]} {self.operationString} {right_table}.{self.rightAttribute.split('.')[1]}"

    def getInvolvedTables(self):
        left_table = self.leftAttribute.split('.')[0]
        right_table = self.rightAttribute.split('.')[0]
        tables = set()
        tables.add(left_table)
        tables.add(right_table)
        return list(tables)

    def getArgs(self, store):
        return []

    def __repr__(self):
        return f"TwoAttributeComparison({self.leftAttribute}, {self.operationString}, {self.rightAttribute})"