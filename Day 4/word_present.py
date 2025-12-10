with open("poems.txt", "r") as f:
    content = f.read()

if "twinkle" in content.lower():
    print("The word 'twinkle' is present.")
else:
    print("The word 'twinkle' is NOT present.")
