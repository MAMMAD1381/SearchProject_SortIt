class Test:
    def __init__(self, name, family):
        self.name = name
        self.family = family

    def __eq__(self, other):
        if (other.name == self.name) and (other.family == self.family):
            return True
        return False


name = Test('ali', 'redd')
test = Test('ali', 'redd')
print(name.__eq__(test))
