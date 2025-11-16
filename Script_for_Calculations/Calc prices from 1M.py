import os
while True:
    TT = float(input("Enter price for 4.8M : "))
    os.system("cls")
    print("JUST DID " , TT)
    BasePrice = TT/4.8
    SuperBasePrice = 2.4 * BasePrice
    print('{0:.2f}'.format(SuperBasePrice) , "-2.4")
    Temp = 3 * BasePrice
    print('{0:.2f}'.format(Temp - SuperBasePrice) , "-3")
    Temp = 3.6 * BasePrice
    print('{0:.2f}'.format(Temp - SuperBasePrice) , "-3.6")
    Temp = 4.8 * BasePrice
    print('{0:.2f}'.format(Temp - SuperBasePrice) , "-4.8")
    