import pandas as pd
from bs4 import * 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
import time
import os
import datetime

import sys
from pathlib import Path
ScriptDir = Path(__file__).parent
InputDir = ScriptDir.parent / "Inputs"
InputDir.mkdir(exist_ok=True)
InputDir = InputDir / "ProductWickesLinks.csv"

InfoDir = ScriptDir.parent / "SensitiveInfo.txt"
Variables = {}
for line in InfoDir.read_text().splitlines():
    key, value = line.split("=")
    Variables[key.strip()] = value.strip()
CardNumber = Variables["CardNumber"]
CVC = Variables["cvc"]
ExpiryMonth = Variables["ExpiryMonth"]
ExpiryYear = Variables["ExpiryYear"]
RegisteredAddress = Variables["RegisteredAddress"]

sys.path.append(str(Path(__file__).resolve().parent.parent))
from Custom_Functions import *


UniversalOptionsLoad()
Driver = MainDriverLoad()
EbayOrderViewDriver = ViewDriverLoad()

WickesLogin(Driver)

Flag = True
ColumnOutline = pd.DataFrame(columns = ["EbayProductName" , "WickesURL"]) 

EbayAwaitingDispatchOrdersURl = r"https://www.ebay.co.uk/sh/ord/?filter=status%3AAWAITING_SHIPMENT&sort=-paiddate"

Driver.get(EbayAwaitingDispatchOrdersURl)
WebDriverWait(Driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//a[@_sp='p2367289.m4322.l155387']"))
)
        
os.system("cls")
os.system("cls")
while(Flag):
    PhoneNumber="07834224872"
    ImportedData = pd.read_csv(InputDir)
    StopOrderOverride = False
    EbayAwaitingDispatchOrderHTML = BeautifulSoup(Driver.page_source , "html.parser")
    CurrentEbayOrder = "https://www.ebay.co.uk/" + EbayAwaitingDispatchOrderHTML.find("a" , href=True , attrs = {"_sp" : "p2367289.m4322.l155387"})["href"]
    print(f"Current worked ebay order : {CurrentEbayOrder}")
    EbayOrderViewDriver.get(CurrentEbayOrder)
    Driver.find_element(By.CSS_SELECTOR , ("[class='fake-menu-button__button icon-btn icon-btn--small']") ).click() 
    Driver.find_element(By.XPATH, "//span[text()='View order details']").click() # Click view order details
    OrderPageHTML = BeautifulSoup(Driver.page_source , "html.parser")
    
    time.sleep(3)                                                     
    ClientName = Driver.find_element(By.XPATH , "(//div[@class='address']//button)[1]").text
    try:
        FirstName , LastName = ClientName.split(" ")
    except:
        FirstName = ClientName
        LastName = ClientName
        
    ClientPhone = OrderPageHTML.find("button" , attrs={"aria-controls" : "s0-1-0-20-9-11-15-66-20-2-15-10-1-1-overlay"}).text # Get phone number
    ClientPhone = ClientPhone.replace("+44 " , "0")
    try:
        Address = OrderPageHTML.find("button" , attrs={"aria-controls" : "s0-1-0-20-9-11-15-64-15[0[1]]-1-1-overlay"}).text # Get first line of address
    except:
        try:
            Address = OrderPageHTML.find("button" , attrs={"aria-controls" : "s0-1-0-20-9-11-15-65-15[0[1]]-1-1-overlay"}).text
        except:
            Address = OrderPageHTML.find("button" , attrs={"aria-controls" : "s0-1-0-20-9-11-15-66-15[0[1]]-1-1-overlay"}).text
       
    Address = re.sub(r"(\d+)([A-Za-z])", r"\1 \2", Address)
    Postcode = Driver.find_element(By.XPATH , "(//div[@class='address']//button)[6]").text 
    FirstLine = Driver.find_element(By.XPATH , "(//div[@class='address']//button)[2]").text
    
    OneStep =  OrderPageHTML.find("div" , attrs={"class" : "payment-info"}) 
    TwoStep = (BeautifulSoup(str(OneStep) , "html.parser")).find("div" , attrs={"class" : "earnings"})
    ThirdStep = (BeautifulSoup(str(TwoStep) , "html.parser")).find("div" , attrs={"class" : "total"})
    FourthStep = (BeautifulSoup(str(ThirdStep) , "html.parser")).find("dd" , attrs={"class" : "amount"}).text
    OrderValue = FourthStep.replace("£" , "")
    try:
        if float(OrderValue) > 100 :
            input(f"Order value is {OrderValue} which is higher than £100. Check if TP or Jewson isnt worth. If isn't press enter")
    except:
        OrderValue = FourthStep.replace("GB " , "")
        if float(OrderValue) > 100 :
            input(f"Order value is {OrderValue} which is higher than £100. Check if TP or Jewson isnt worth. If isn't press enter")
            
        
        
    ProductNames = []
    ProductQuantitys = []
    InternalProductNames = []
    ItemCardCount = OrderPageHTML.findAll("div" , attrs={"class" : "item-card"}) # Get all prodcut cards
    for ProductCard in ItemCardCount:
        ProductCard = BeautifulSoup(str(ProductCard) , "html.parser")
        ProductNames.append(ProductCard.find("a" , attrs={"_sp" : "p4256617.m146416.l8116"}).text) # Get product name
        ProductQuantity = ProductCard.find("div" , attrs={"class" : "quantity__value"}).text # Get product quantity tag text
        ProductQuantitys.append(ProductQuantity.split("(")[0])
        
        #Try get any product options
        try: #Are options
            AllProductOptions = ProductCard.find("div" , attrs={"class" : "lineItemCardInfo__aspects spaceTop"}).text
            try: #Double options
                FirstProductOption , SecondProductOption = AllProductOptions.split(" ·")
                FirstProductOptionName , FirstProductOptionID = FirstProductOption.Split (": ")
                SecondProductOptionName , SecondProductOptionID = SecondProductOption.spilt(": ")
                if FirstProductOption.lower() == "pack quantity" or SecondProductOptionName.lower() == "pack quantity":
                    StopOrderOverride = True
                InternalProductName = ProductNames[-1] + "_______*******_______" + FirstProductOptionID + "_______*******_______" + SecondProductOptionID
                InternalProductNames.append(InternalProductName)
            except: #Single option
                FirstProductOption = AllProductOptions
                FirstProductOptionName , FirstProductOptionID = FirstProductOption.split(": ")
                if FirstProductOption.lower() == "pack quantity":
                    StopOrderOverride = True
                InternalProductName = ProductNames[-1] + "_______*******_______" + FirstProductOptionID
                InternalProductNames.append(InternalProductName)
            
        except: # No options
            InternalProductName = ProductNames[-1]
            InternalProductNames.append(InternalProductName)
            
    PrintabeOrder = ""
    for i in range(len(ProductNames)):
        if i > 0:
            PrintabeOrder = PrintabeOrder + " & "
        PrintabeOrder = PrintabeOrder + ProductQuantitys[i] + " " + ProductNames[i] 
        
    for i in range(len(ProductNames)):  
        FoundRows = ImportedData[ImportedData["EbayProductName"] == InternalProductNames[i]]
        if len(FoundRows) == 0: #If no found product
            WantToAdd = ""
            while WantToAdd != "Y" and WantToAdd != "N":
                WantToAdd = input(f"There was no found url for product {InternalProductNames[i]} , would you like to enter a url for it ? Y/N : ")
            if WantToAdd == "N":
                pass
            else:
                NewURLData = {
                "EbayProductName": InternalProductNames[i],
                "WickesURL": input("please enter the url of the wickes product : ")
                }
                ImportedData = ImportedData._append(NewURLData, ignore_index=True)
                ImportedData.to_csv(InputDir , index = False)
                print("Data successfully added, will try order again")
    
    WickesDoableOrderIndexes = []
    for i in range(len(ProductNames)):  
        FoundRows = ImportedData[ImportedData["EbayProductName"] == InternalProductNames[i]]
        if len(FoundRows) == 0: #If no found product
            input(f"There is a product that can't be delivered by Wickes, product is {InternalProductNames[i]} \nProceed by pressing enter : ")
        elif "MINIMUM" in InternalProductNames[i]:
            input(f"There is a product that can't be delivered because of minimum order check, product is {InternalProductNames[i]} \nProceed by pressing enter : ") 
        else:
            WickesDoableOrderIndexes.append(i)
            
    if len(WickesDoableOrderIndexes) != len(InternalProductNames):
        StopOrderOverride = True
        
        
    if StopOrderOverride == False:
        Driver.get(r"https://www.wickes.co.uk/cart")
        time.sleep(5)
        try:
            while (True):
                try:
                    Driver.find_elements(By.XPATH, "//button[@class='btn order-item__remove']")[0].click()
                    time.sleep(5)
                except:
                    Driver.find_elements(By.XPATH, "//button[@class='btn order-item__remove']")[1].click()
                    time.sleep(5)
        except:
            pass
            
    for ProductIndex in WickesDoableOrderIndexes:
        ProductQuantity = ProductQuantitys[ProductIndex]
        
        FoundRows = ImportedData[ImportedData["EbayProductName"] == InternalProductNames[ProductIndex]]
        ProductURL = FoundRows.iloc[0]["WickesURL"]
        
        
        Driver.get(ProductURL)
        time.sleep(3)
        QuantityInput = Driver.find_element(By.CSS_SELECTOR , "[class='tbx tbx_quantity']")     
        QuantityInput.send_keys(Keys.BACKSPACE)
        QuantityInput.send_keys(ProductQuantitys[ProductIndex])
        time.sleep(2)
        try:
            Driver.find_element(By.CSS_SELECTOR , "[class='btn btn-action btn_full btn-add-to-basket BGAAListener']").click()
        except:
            Driver.find_element(By.CSS_SELECTOR , "[class='btn btn-action btn_full btn-add-to-basket']").click()
    
    if WickesDoableOrderIndexes != []:
            
        ### checkout sequence
        Driver.get(r"https://www.wickes.co.uk/cart")
        time.sleep(3)
        Driver.get(r"https://www.wickes.co.uk/cart/checkout")
        time.sleep(3)
        WickesCheckoutPageHTML = BeautifulSoup(Driver.page_source , "html.parser")
        try:
            CheckoutTotal = WickesCheckoutPageHTML.find("div" , attrs={"class" : "checkout-widget__total"}).text
        except: 
            input("Login and enter when done : ")
        WickesCheckoutPageHTML = BeautifulSoup(Driver.page_source , "html.parser")
        CheckoutTotal = WickesCheckoutPageHTML.find("div" , attrs={"class" : "checkout-widget__total"}).text
            
        CheckoutTotal = CheckoutTotal.replace("£" , "")
        CheckoutTotal = ''.join([char for char in CheckoutTotal if char.isdigit() or char=="."])
        if float(OrderValue) < float(CheckoutTotal):
            print("BUY PRICE IS HIGHER THAN REVENUE, check if it should go through")
            input("Enter to continue : ")
        if StopOrderOverride == False:
            try:
                dropdown = Select(Driver.find_element("class name", "v-select"))  
            except:
                Driver.find_element(By.XPATH, "//div[@data-id='open-delete-confirmation']").click()
                time.sleep(1)
                Driver.find_element(By.XPATH, "//span[text()='Yes, delete']").click()
                time.sleep(3)
                dropdown = Select(Driver.find_element("class name", "v-select")) 
            
            dropdown.select_by_visible_text("Mx")
            Driver.find_element(By.CSS_SELECTOR , "[autocomplete='given-name']").send_keys(FirstName)
            Driver.find_element(By.CSS_SELECTOR , "[autocomplete='family-name']").send_keys(LastName)
            Driver.find_element(By.CSS_SELECTOR , "[tabindex='40']").send_keys(PhoneNumber)
            # Driver.find_element(By.CSS_SELECTOR , ("[tabindex='50']") ) .send_keys("") HOME PHONE
            Driver.find_element(By.CSS_SELECTOR , "[tabindex='60']") .send_keys(Postcode + FirstLine)
            AllAddressOptions = Driver.find_elements(By.XPATH , "//li[@role='option']")
            if len(AllAddressOptions) != 0 :
                pass
            else:
                time.sleep(1)
                try:
                    Driver.find_element(By.XPATH , "//li[@role='option']").click()
                    time.sleep(1)
                    input("Check if its got delivery address right")
                    Driver.find_element(By.XPATH, "//button[@id='submitAddressButton']").click()
                    time.sleep(3)
                except:
                    input("Enter a delivery address")
                    Driver.find_element(By.XPATH, "//button[@id='submitAddressButton']").click()
                    time.sleep(3)
                
            Driver.find_element(By.XPATH , "//div[@class='checkout-widget__voucher-toggle collapsed']").click()
            time.sleep(1)
            Driver.find_element(By.XPATH , "(//div[@class='v-form-row__field'])[2]/input").send_keys("TRADEPRO")
            Driver.find_element(By.XPATH , "//button[@data-id='submit-voucher-button']").click()
            time.sleep(5)  
            
            Driver.find_element(By.XPATH , "//button[@data-id='next-step-button']").click()
            WebDriverWait(Driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@data-slot-available-for-grouping='true']"))
                )
            time.sleep(1)
            DeliveryAddressPageHTML = BeautifulSoup(Driver.page_source , "html.parser")
            SelectableDates = DeliveryAddressPageHTML.findAll("span" , attrs = {"data-slot-available-for-grouping" : "true"})
            if len(SelectableDates) == 0: #No dates
                SelectableDates = DeliveryAddressPageHTML.findAll("span" , attrs = {"data-slot-available-for-grouping" : "True"})
                if len(SelectableDates) == 0: #No dates
                    input("No available delivery date, manually enter details and ensure 100% no delivery" + "\n" + "Press any button to continue program by trying to find another order awaiting delivery")
            else: #Are dates
                GoodDateID = None
                for AvaialbleDeliveryDate in SelectableDates:
                    WorkedDay = AvaialbleDeliveryDate.text
                    WorkedDay = ''.join([char for char in WorkedDay if char.isdigit()])
                    WorkedMonth = str(datetime.datetime.now().month)
                    if int(WorkedDay) < int(datetime.datetime.now().day):
                        WorkedMonth = str(int(datetime.datetime.now().month) + 1)
                    if WorkedMonth == "13":
                        WorkedMonth = "01"

                    if len(WorkedDay) == 1:
                        WorkedDay = "0" + WorkedDay
                    if len(WorkedMonth) == 1:
                        WorkedMonth = "0" + WorkedMonth
                    date_string = f"2025-{WorkedMonth}-{WorkedDay}"  
                    date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d")
                    uk_format = date_obj.strftime("%d/%m/%Y")
                    day_name = date_obj.strftime("%A")
                    if day_name != "Saturday" and day_name != "Sunday":
                        GoodDateID = AvaialbleDeliveryDate["id"]
                        Driver.find_element(By.XPATH, f"//span[@id='{GoodDateID}']").click()
                        break
            time.sleep(1)            
            DeliveryPrice = DeliveryAddressPageHTML.find("span" , attrs = {"id" : "order-delivery-1"}).text
            DeliveryPrice = re.sub(r"[\n\t\s]+", "", DeliveryPrice).strip()  # Replace \n, \t, and extra spaces with single space
            if DeliveryPrice != "£4.00":
                input("Please check delivery price/date, if anything wrong JUST selct date new better date.")
                            
            
            Driver.find_element(By.XPATH , "//button[@class='btn btn-action submit-btn']").click()
            time.sleep(5)
            Driver.find_element(By.XPATH, "//input[@id='card_nameOnCard']").clear()
            Driver.find_element(By.XPATH, "//input[@id='card_nameOnCard']").send_keys("lukasz pawel ilnicki")
            Driver.find_element(By.XPATH, "//input[@id='card_nameOnCard']").clear()
            Driver.find_element(By.XPATH, "//input[@id='card_nameOnCard']").send_keys("lukasz pawel ilnicki")
            Driver.find_element(By.XPATH, "//input[@id='address-lookup-query']").send_keys(RegisteredAddress)
            time.sleep(1)
            Driver.find_element(By.XPATH , "//li[@role='option']").click()
            time.sleep(1)
            Driver.find_element(By.XPATH , "//button[@form='hopPaymentAddressPostForm']").click()
            time.sleep(5)
            
            Driver.switch_to.frame("hopIframe")  # Replace with actual iframe ID
            Driver.find_element(By.XPATH, "//input[@id='cardNumber']").clear() 
            Driver.find_element(By.XPATH, "//input[@id='cardNumber']").send_keys(CardNumber)
            time.sleep(1)
            Driver.find_element(By.XPATH, "//input[@id='csc']").send_keys(CVC)
            dropdown = Select(Driver.find_element(By.ID, "expiryMonth"))  
            time.sleep(1)
            dropdown.select_by_visible_text(ExpiryMonth)
            
            dropdown = Select(Driver.find_element(By.ID, "expiryYear"))  
            time.sleep(1)
            dropdown.select_by_visible_text(ExpiryYear)
            time.sleep(1)
            Driver.find_element(By.XPATH , "//div[@id='paynowButtonHolder']").click()
            print("Confirm payment")
            
            WebDriverWait(Driver, 999).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='header__order-number']"))
            )
        
            OrderConfirmationPageHTML = BeautifulSoup(Driver.page_source , "html.parser")
            WickesOrderNumber = OrderConfirmationPageHTML.find("span" , attrs={"class" : "header__order-number"}).text
            Driver.get(CurrentEbayOrder)
            time.sleep(3)
            Driver.find_element(By.XPATH, "//button[@class='menu-button__button btn btn--secondary']").click()
            try:
                Driver.find_elements(By.XPATH, "//div[@data-action-id='ADD_NOTE']")[1].click()
            except:
                try:
                    Temp = Driver.find_element(By.XPATH , "//span[@id='nid-cjw-19']")
                    Temp.find_element(By.XPATH, "//button[@aria-controls='nid-jyk-16-content']").click()
                    Temp.find_elements(By.XPATH, "//div[@data-action-id='ADD_NOTE']").click()
                except:
                    Temp== Driver.find_element(By.XPATH , "//span[@id='Empnid-ul7-18']")
                    Temp.find_element(By.XPATH  ,"//button[@aria-controls='nid-ul7-18-content']").click()
                    Temp.find_elements(By.XPATH, "//div[@data-action-id='ADD_NOTE']")[1].click()
                
            time.sleep(1)  
            Driver.find_element(By.XPATH, "//textarea[@aria-label='My note']").send_keys("Wickes order number : " + WickesOrderNumber)
            time.sleep(1)
            Driver.find_element(By.XPATH, "//button[text()='Save']").click()
            time.sleep(2)  
            Driver.find_element(By.XPATH, "//button[@class='menu-button__button btn btn--secondary']").click()
            Driver.find_elements(By.XPATH, "//div[@data-action-id='MARK_SHIPPED']")[1].click()
            time.sleep(2)
            Driver.back()
            
            Driver.find_element(By.XPATH, "//a[@class='fake-btn fake-btn--secondary']").click()
            WebDriverWait(Driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='imageupload__inputmultiline']")))
            Driver.find_element(By.XPATH, "//textarea[@id='imageupload__sendmessage--textbox']").send_keys(f"Your order of {PrintabeOrder} will arrive on {uk_format}")
            time.sleep(1)
            input("Check message")
            Driver.find_element(By.XPATH, "//button[@id='imageupload__send--button']").click()
            time.sleep(3)
    
            Driver.get(EbayAwaitingDispatchOrdersURl)
            WebDriverWait(Driver, 40).until(
                EC.presence_of_element_located((By.XPATH, "//a[@_sp='p2367289.m4322.l155387']"))
                )
            EbayAwaitingDispatchOrderHTML = BeautifulSoup(Driver.page_source , "html.parser")
            
            while CurrentEbayOrder == ("https://www.ebay.co.uk/" + EbayAwaitingDispatchOrderHTML.find("a" , href=True , attrs = {"_sp" : "p2367289.m4322.l155387"})["href"]):
                time.sleep(3)
                Driver.get(EbayAwaitingDispatchOrdersURl)
                WebDriverWait(Driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@_sp='p2367289.m4322.l155387']"))
                    )
                EbayAwaitingDispatchOrderHTML = BeautifulSoup(Driver.page_source , "html.parser")
            
            
                
            
        
        
        
        
    os.system("cls")
    os.system("cls")
    pass
    


    
