import os
BasePrice = float(input("Input base price : "))
while True:
    try:
        NextTotalPrice = float(input("Input next total price : "))
        if NextTotalPrice == 0:
            os.system("cls")
            os.system("cls")
            BasePrice = float(input("Input base price : "))
        else:
            print('{0:.2f}'.format(NextTotalPrice - BasePrice))
    except:
        pass