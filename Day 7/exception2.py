try:
    with open("a.txt", "r") as f1:
        with open("b.txt", "w") as f2:
            f2.write(f1.read())
    print("File copied")
except Exception as e:
    print(e)
