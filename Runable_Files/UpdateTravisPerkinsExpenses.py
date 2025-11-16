import pandas as pd
from bs4 import * 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

import sys
from pathlib import Path
ScriptDir = Path(__file__).parent
OutputDir = ScriptDir.parent / "Outputs"
OutputDir.mkdir(exist_ok=True)
OutputDir = OutputDir / "TravisPerkinsOrderExpenses.csv"

sys.path.append(str(Path(__file__).resolve().parent.parent))
from Custom_Functions import *

UniversalOptionsLoad()
Driver = MainDriverLoad()

TravisPerkinsLogin(Driver)

Driver.get(r"https://www.travisperkins.co.uk/accountDashboard/orderHistory/1/10")
WebDriverWait(Driver, 5).until(
    EC.presence_of_element_located((By.XPATH , "//div[@data-test-id='orders-list-item']") )
    )
Flag = True
TravisOrderNumbers = []
TravisURLs = []
TravisExpenses = []
TravisDates = []
while Flag:
    WorkedURL = Driver.current_url
    OrderDivs = Driver.find_elements(By.XPATH , "//div[@data-test-id='orders-list-item']")
    original_window = Driver.current_window_handle
    for i in range(len(OrderDivs)):
        ReloadedOrderDivs = Driver.find_elements(By.XPATH , "//div[@data-test-id='orders-list-item']")[i].click()
        WebDriverWait(Driver, 5).until(
            EC.presence_of_element_located((By.XPATH , "//div[@class='OrderDetailsSidebar__SidebarItem-sc-txg47c-2 OrderDetailsSidebar__SidebarPriceTotal-sc-txg47c-6 gOuzgi cpCAJz noibu-blocked']") )
            )
        OrderPage = BeautifulSoup(Driver.page_source , "html.parser")
        
        OrderNumber = OrderPage.find("h1" , attrs={"class" : "sc-aXZVg sc-gEvEer gUauWZ kGWDjd"}).text
        
        PriceBar = OrderPage.find("div" , attrs={"class" : "OrderDetailsSidebar__SidebarItem-sc-txg47c-2 OrderDetailsSidebar__SidebarPriceTotal-sc-txg47c-6 gOuzgi cpCAJz noibu-blocked"})
        PriceBar = BeautifulSoup(str(PriceBar) , "html.parser")
        OrderPrice = PriceBar.findAll("span" , attrs={"color" : "text-default"})[1].text
        OrderPrice = OrderPrice.replace("£" , "")
        OrderPrice = float(OrderPrice)
        
        OrderURL = Driver.current_url
        
        OrderDate = OrderPage.find("span" , attrs={"class" : "sc-aXZVg sc-kpDqfm cTYWJP bWcTac"}).text
        OrderDate = datetime.datetime.strptime(OrderDate , "%d %B, %Y %H:%M")
        
        TravisOrderNumbers.append(OrderNumber)
        TravisURLs.append(OrderURL)
        TravisExpenses.append(OrderPrice)
        TravisDates.append(OrderDate)
        Driver.get(WorkedURL)
        WebDriverWait(Driver, 5).until(
            EC.presence_of_element_located((By.XPATH , "//div[@data-test-id='orders-list-item']") )
            )
        
    Driver.find_element(By.XPATH  ,"//div[@data-test-id='orders-pagination-next-btn']").click()
    time.sleep(2)
    if WorkedURL == Driver.current_url:
        Flag = False
        Driver.quit()

SendData = {
          "Travis Perkins Order Number": TravisOrderNumbers,
          "Travis Perkins URL": TravisURLs, 
          "Date" : TravisDates,
          "Expense" : TravisExpenses
        }

df = pd.DataFrame(SendData)

df.to_csv(OutputDir , index = False)       