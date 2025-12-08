def sum_natural(n):
    if n == 1:
        return 1
    else:
        return n + sum_natural(n - 1)


n = int(input("Enter a number: "))
print(f"sum of {n} number is {sum_natural(n)}")