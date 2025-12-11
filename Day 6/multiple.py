class A:
    def feature_a(self):
        return "Feature A"

class B:
    def feature_b(self):
        return "Feature B"

class C(A, B):
    pass

obj = C()
print(obj.feature_a())
print(obj.feature_b())
