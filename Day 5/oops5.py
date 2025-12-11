class Person:
    species = "Human"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @staticmethod
    def is_adult(age):
        return age >= 18

    def details(self):
        return f"{self.name}, {self.age}, {self.species}"

p1 = Person("Abhimanyu", 18)
print(p1.details())
print(Person.is_adult(p1.age))
print(Person.species)
