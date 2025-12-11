class Bird:
    def fly(self):
        return "Bird can fly"

class Sparrow(Bird):
    def fly(self):
        return "Sparrow flies fast"

class Penguin(Bird):
    def fly(self):
        return "Penguin cannot fly"

animals = [Bird(), Sparrow(), Penguin()]

for a in animals:
    print(a.fly())
