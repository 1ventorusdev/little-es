import os
import sys

print("test2")
print(os.getcwd())

while True: 
    restart = input(">>>")

    if restart == "restart":
        os.execv(sys.executable, ['python3'] + sys.argv)
    elif restart == "close":
        quit()
    else:
        print("non")