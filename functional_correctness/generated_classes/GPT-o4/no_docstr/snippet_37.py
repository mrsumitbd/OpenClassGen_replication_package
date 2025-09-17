class TwoAttributeComparison:

    def __init__(self, leftAttribute, operationString, rightAttribute):
        self.leftAttribute = leftAttribute
        self.operationString = operationString
        self.rightAttribute = rightAttribute

    def getQuery(self, store):
        left_q = self.leftAttribute.getQuery(store)
        right_q = self.rightAttribute.getQuery(store)
        return f"{left_q} {self.operationString} {right_q}"

    def getInvolvedTables(self):
        return self.leftAttribute.getInvolvedTables().union(
            self.rightAttribute.getInvolvedTables()
        )

    def getArgs(self, store):
        return self.leftAttribute.getArgs(store) + self.rightAttribute.getArgs(store)

    def __repr__(self):
        return (
            f"TwoAttributeComparison({self.leftAttribute!r}, "
            f"{self.operationString!r}, {self.rightAttribute!r})"
        )