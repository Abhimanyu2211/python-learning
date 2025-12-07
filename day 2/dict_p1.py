
dict = {
    "पानी": "water",
    "किताब": "book",
    "घर": "house"
}

word = input("Enter a Hindi word: ")

print("Meaning:", dict.get(word, "Word not found"))
