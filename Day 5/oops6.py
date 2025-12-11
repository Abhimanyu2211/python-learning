class Student:
    def __init__(self, name, marks):
        self.name = name
        self.__marks = marks

    def get_marks(self):
        return self.__marks

    def set_marks(self, new_marks):
        if new_marks >= 0:
            self.__marks = new_marks

s = Student("Abhimanyu", 85)
print(s.name)
print(s.get_marks())
s.set_marks(90)
print(s.get_marks())
