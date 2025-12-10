n = int(input("Enter n: "))

with open("sample.txt", "r") as f:
    for i in range(n):
        print(f.readline(), end="")
