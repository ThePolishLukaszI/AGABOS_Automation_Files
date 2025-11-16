import pandas as pd
from bs4 import * 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import sys
from pathlib import Path
ScriptDir = Path(__file__).parent
OutputDir = ScriptDir.parent / "Outputs"
OutputDir.mkdir(exist_ok=True)
OutputDir = OutputDir / "WickesOrdersTypes.csv"

sys.path.append(str(Path(__file__).resolve().parent.parent))
from Custom_Functions import *

UniversalOptionsLoad()
Driver = MainDriverLoad()

WickesLogin(Driver)

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
WickesOrderTypes = []
WickesOrderURLs = []
ExtraDetails = []
for CurrentOrderDiv in AllOrderDivs:
    CurrentOrderDivHTML = BeautifulSoup(str(CurrentOrderDiv) , "html.parser")
    CurrentOrderURL = CurrentOrderDivHTML.find("a" , href=True , attrs = {"class" : "btn btn-full btn-primary"})["href"]
    Driver.get(r"https://www.wickes.co.uk/" + CurrentOrderURL)
    WebDriverWait(Driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='icon']"))
    )
    
    CurrentOrderHTML = BeautifulSoup(Driver.page_source , "html.parser")
    OrderType = "TBD"
    
    if CurrentOrderHTML.find("svg" , attrs={"data-icon" : "info-circle"}) is None: 
        if CurrentOrderHTML.find("svg" , attrs={"data-icon" : "times-circle"}) is None:
            OrderType = "BAD ARRAY"
        else:
            OrderType = "bad"
    else:
        OrderType = "good"
            
    if OrderType == "bad":
        print(f"Order URL https:/www.wickes.co.uk{CurrentOrderURL} has order type of {OrderType}")
           
    WickesCurrentOrderNumber = CurrentOrderHTML.find("span" , attrs={"class" : "order-heading__value"}).text
    WickesOrderNumbers.append(WickesCurrentOrderNumber)
    WickesOrderTypes.append(OrderType)
    WickesOrderURLs.append(r"https://www.wickes.co.uk/" + CurrentOrderURL)
    
    Father = CurrentOrderHTML.find("div" , attrs={"class" : "wismo__order-pay wismo__order-right"})
    Father = BeautifulSoup(str(Father) , "html.parser")
    delivery_div = Father.findAll(lambda tag: tag.name == "div" and "Delivery address" in tag.text)[1]
    delivery_name = delivery_div.find_next("div", class_="wrap-item__value").get_text("\n", strip=True).split("\n")[0]
    ExtraDetails.append(delivery_name) 
    
    

SendData = {
          "Wickes Order Number": WickesOrderNumbers,
          "Wickes URL": WickesOrderURLs, 
          "Order Type" : WickesOrderTypes,
          "Extra Details" : ExtraDetails
        }

df = pd.DataFrame(SendData)

df.to_csv(OutputDir, index = False)           
            
        
    
    
