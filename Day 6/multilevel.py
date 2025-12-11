class A:
    def method_a(self):
        return "A"

class B(A):
    def method_b(self):
        return "B"

class C(B):
    def method_c(self):
        return "C"

obj = C()
print(obj.method_a())
print(obj.method_b())
print(obj.method_c())
