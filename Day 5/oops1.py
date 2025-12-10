class Student:
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

s1 = Student()
s1.set_name("Abhimanyu")
print(s1.get_name())
