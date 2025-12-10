with open("story.txt", "r") as f:
    text = f.read()

lines = text.count("\n") + 1
words = len(text.split())
chars = len(text)

print("Lines:", lines)
print("Words:", words)
print("Characters:", chars)
