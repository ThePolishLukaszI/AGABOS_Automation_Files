import pandas as pd
from bs4 import * 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
import datetime
import sys
from pathlib import Path
ScriptDir = Path(__file__).parent
OutputDir = ScriptDir.parent / "Outputs"
OutputDir.mkdir(exist_ok=True)
OutputDir = OutputDir / "WickesOrderExpenses.csv"

sys.path.append(str(Path(__file__).resolve().parent.parent))
from Custom_Functions import *

UniversalOptionsLoad()
Driver = MainDriverLoad()

LoginModules.WickesLogin(Driver)

Flag = True

Driver.get(r"https://www.wickes.co.uk/my-account/orders")
time.sleep(5)
try:
    while(True):
        Driver.find_element(By.XPATH, "//button[@class='btn btn-primary load-more']").click()
        time.sleep(1)
except:
    pass

WickesOrdersPageHTML = BeautifulSoup(Driver.page_source , "html.parser")
AllOrderDivs = WickesOrdersPageHTML.findAll("div" , attrs={"class" : "wismo-hist__table"})

WickesOrderNumbers = []
WickesOrderURLs = []
WickesDates = []
WickesOrderCosts = []
WickesDeliveryAddresses = []
WickesIsRefunded = []
WickesIsMaybeDuplicate = []
Names = []
for CurrentOrderDiv in AllOrderDivs:
    CurrentOrderDivHTML = BeautifulSoup(str(CurrentOrderDiv) , "html.parser")
    CurrentOrderURL = CurrentOrderDivHTML.find("a" , href=True , attrs = {"class" : "btn btn-full btn-primary"})["href"]
    Driver.get(r"https://www.wickes.co.uk/" + CurrentOrderURL)
    WebDriverWait(Driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='icon']"))
    )
    
    CurrentOrderHTML = BeautifulSoup(Driver.page_source , "html.parser")
           
    WickesCurrentOrderNumber = CurrentOrderHTML.find("span" , attrs={"class" : "order-heading__value"}).text
    WickesCurrentOrderNumber = WickesCurrentOrderNumber.replace(" " , "")
    WickesOrderNumbers.append(WickesCurrentOrderNumber)
    WickesOrderURLs.append(r"https://www.wickes.co.uk/" + CurrentOrderURL)
    
    if WickesCurrentOrderNumber == "678686943":
        print("")
    Father = CurrentOrderHTML.find("div" , attrs={"class" : "wismo__order-pay wismo__order-right"})
    Father = BeautifulSoup(str(Father) , "html.parser")
    delivery_div = Father.findAll(lambda tag: tag.name == "div" and "Delivery address" in tag.text)[1]
    delivery_name = delivery_div.find_next("div", class_="wrap-item__value").get_text("\n", strip=True).split("\n")[0]
    Names.append(delivery_name) 
    
    Father = CurrentOrderHTML.findAll("div" , attrs={"class" : "order-heading__info"})[1]
    Father = BeautifulSoup(str(Father) , "html.parser")
    date = Father.find("span" , attrs={"class" : "order-heading__value"}).text
    date = date.strip()
    date = datetime.datetime.strptime(date , "%B %d, %Y - %I:%M %p")
    WickesDates.append(date)
    
    OrderCost = CurrentOrderHTML.find("div" , attrs={"class" : "total__value"}).text
    OrderCost = OrderCost.replace("£" , "")
    WickesOrderCosts.append(OrderCost)
    
    if CurrentOrderHTML.find("h3" , attrs={"class" : "wismo-order__delivery-notification qa_wismo-order__delivery-notification-fail"}) is not None:
        NotifTag = CurrentOrderHTML.find("h3" , attrs={"class" : "wismo-order__delivery-notification qa_wismo-order__delivery-notification-fail"})
        NotifTag = BeautifulSoup(NotifTag.text , "html.parser")
        if NotifTag.find("svg" , attrs={"data-icon" : "check-circle"}) is not None: 
            WickesIsRefunded.append("Refunded")
        else:
            WickesIsRefunded.append("Valid")
    else:
        WickesIsRefunded.append("Valid")
        
    DeliveryAdress = CurrentOrderHTML.find_all("div" , attrs={"class" : "wrap-item__value"})[5].text
    if DeliveryAdress in WickesDeliveryAddresses:
        WickesIsMaybeDuplicate.append("True")
    else:
        WickesIsMaybeDuplicate.append("False")
        
    WickesDeliveryAddresses.append(DeliveryAdress)

SendData = {
          "Wickes Order Number": WickesOrderNumbers,
          "Wickes URL": WickesOrderURLs, 
          "Date" : WickesDates,
          "Expense" : WickesOrderCosts,
          "Delivery Address" : WickesDeliveryAddresses,
          "Is Refunded?" : WickesIsRefunded
        }

df = pd.DataFrame(SendData)

df.to_csv(OutputDir , index = False)           
            
        
    
    
