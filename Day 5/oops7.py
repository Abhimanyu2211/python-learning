class Bank:
    def __init__(self, balance):
        self.__balance = balance

    def __update_balance(self, amount):
        self.__balance += amount

    def deposit(self, amount):
        self.__update_balance(amount)
        return self.__balance

b = Bank(1000)
print(b.deposit(500))
