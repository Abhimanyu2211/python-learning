lst = list(map(int, input().split()))
key = int(input())

found = False
for i in lst:
    if i == key:
        found = True
        break

print("Found" if found else "Not Found")
