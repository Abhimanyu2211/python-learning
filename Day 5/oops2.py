class Demo:
    class_attr = "Class Attribute"

    def __init__(self, value):
        self.instance_attr = value

    @staticmethod
    def static_method():
        return "Static Method"

d = Demo("Instance Attribute")
print(Demo.class_attr)
print(d.instance_attr)
print(Demo.static_method())
