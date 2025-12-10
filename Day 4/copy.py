with open("source.txt", "r") as src:
    data = src.read()

with open("copy.txt", "w") as dst:
    dst.write(data)

print("File copied successfully.")
