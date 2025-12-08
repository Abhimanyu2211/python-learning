import random

youDict = {"snake": -1, "water": 1, "gun": 0}
reverseDict = {-1: "snake", 1: "water", 0: "gun"}

total_com = 0
total_us = 0

for i in range(1, 4):

    print(f"\n Round {i}")

    computer = random.choice([1, -1, 0])
    you = input("enter your choice (snake/water/gun): ")

    yournum = youDict[you]

    print(f"your choice is {reverseDict[yournum]} and computer choice is {reverseDict[computer]}")

    com = 0
    us = 0

    # game conditions start
    if yournum == computer:
        print("game is draw")

    else:
        if computer == 1 and yournum == -1:
            print("you loose this match")
            com += 1

        elif computer == 1 and yournum == 0:
            print("you win this match")
            us += 1

        elif computer == -1 and yournum == 1:
            print("you win this match")
            us += 1

        elif computer == -1 and yournum == 0:
            print("you loose this match")
            com += 1

        elif computer == 0 and yournum == 1:
            print("you loose this match")
            com += 1

        elif computer == 0 and yournum == -1:
            print("you win this match")
            us += 1

        else:
            print("something got wrong")

    total_com += com
    total_us += us

    print(f"score this round, computer: {com}, you: {us}")

# Final total score after 3 rounds
print("\nfinal result is :")
print(f"Computer total score: {total_com}")
print(f"Your total score: {total_us}")
