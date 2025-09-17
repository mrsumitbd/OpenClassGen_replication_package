class TwoAttributeComparison:
    def __init__(self, leftAttribute, operationString, rightAttribute):
        self.leftAttribute = leftAttribute
        self.operationString = operationString
        self.rightAttribute = rightAttribute

    def getQuery(self, store):
        left_table = self.leftAttribute.split('.')[0]
        right_table = self.rightAttribute.split('.')[0]
        left_column = self.leftAttribute.split('.')[1]
        right_column = self.rightAttribute.split('.')[1]
        
        return f"{left_table}.{left_column} {self.operationString} {right_table}.{right_column}"

    def getInvolvedTables(self):
        left_table = self.leftAttribute.split('.')[0]
        right_table = self.rightAttribute.split('.')[0]
        return {left_table, right_table}

    def getArgs(self, store):
        return []

    def __repr__(self):
        return f"TwoAttributeComparison({self.leftAttribute}, {self.operationString}, {self.rightAttribute})"