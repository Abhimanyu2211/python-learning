old = "bad"
new = "good"

with open("text.txt", "r") as f:
    data = f.read()

data = data.replace(old, new)

with open("text.txt", "w") as f:
    f.write(data)

print("Word replaced.")
