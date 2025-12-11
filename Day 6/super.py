class Parent:
    def __init__(self):
        self.value = "Parent constructor"

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.child_value = "Child constructor"

c = Child()
print(c.value)
print(c.child_value)
