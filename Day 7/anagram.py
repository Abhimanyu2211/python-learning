s1 = input()
s2 = input()

print("Anagram" if sorted(s1) == sorted(s2) else "Not Anagram")
