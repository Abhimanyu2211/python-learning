try:
    n = int(input("Enter a number: "))
    print(10 / n)
except ZeroDivisionError:
    print("Cannot divide by zero")
except ValueError:
    print("Invalid input")
