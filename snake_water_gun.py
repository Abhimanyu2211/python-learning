# -1 is for snake 
# 1 is for water 
# 0 is for gun
import random #using this beacuse i want that computer choose random number every time when we play this game
computer=random.choice([1,-1,0])
you=input("enter your choice:")
youDict={"snake":-1, "water":1, "gun":0}
reverseDict={-1:"snake", 1:"water", 0:"gun"}
yournum=youDict[you]
print(f"your choice is {reverseDict[yournum]} and computer choice is {reverseDict[computer]}")
#game condition start from here 
if yournum==computer:
    print("game is draw")
else:
    if computer==1 and yournum==-1:
        print("you loose this match")
    elif  computer==1 and yournum==0: 
        print("you win this match")
    elif  computer==-1 and yournum==1: 
         print("you win this match")
    elif  computer==-1 and yournum==0: 
        print("you loose this match")
    elif  computer==0 and yournum==1: 
        print("you loose this match")
    elif  computer==0 and yournum==-1:  
         print("you win this match")        
    else:
        print("something got wrong")        