class Parent:
    def show_parent(self):
        return "Parent class"

class Child(Parent):
    def show_child(self):
        return "Child class"

c = Child()
print(c.show_parent())
print(c.show_child())
