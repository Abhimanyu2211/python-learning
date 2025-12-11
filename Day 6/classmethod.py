class Student:
    college = "ABC College"

    def __init__(self, name):
        self.name = name

    @classmethod
    def change_college(cls, new_name):
        cls.college = new_name

s1 = Student("Abhimanyu")
Student.change_college("XYZ College")
print(s1.college)
