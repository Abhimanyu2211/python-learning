class Account:
    def __init__(self, name, balance):
        self.name = name
        self.__balance = balance
        print("Account created")

    def __calculate_interest(self):
        return self.__balance * 0.05

    def add_interest(self):
        self.__balance += self.__calculate_interest()
        return self.__balance

    def get_balance(self):
        return self.__balance

    def remove_balance_attribute(self):
        del self.__balance

    def __del__(self):
        print("Account deleted")

a = Account("Abhimanyu", 2000)
print(a.get_balance())
print(a.add_interest())
a.remove_balance_attribute()
del a
