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
OutputDir = OutputDir / "JewsonsOrderExpenses.csv"

sys.path.append(str(Path(__file__).resolve().parent.parent))
from Custom_Functions import *

UniversalOptionsLoad()
Driver = MainDriverLoad()
JewsonsLogin(Driver)

OrderInstanceDriver = ViewDriverLoad()
JewsonsLogin(OrderInstanceDriver)

Driver.get(r"https://www.jewson.co.uk/my-account/orders/filter?dateFrom=18%2F03%2F2025&amountFrom=0&amountTo=9999&")
WebDriverWait(Driver, 5).until(
    EC.presence_of_element_located((By.XPATH , "//input[@id='dateTo']") )
    )

Driver.find_element(By.XPATH , "//input[@id='dateTo']").click()
time.sleep(1)
try:
    while True:
        Driver.find_elements(By.XPATH , "//span[@class='flatpickr-next-month']")[1].click()
        time.sleep(0.5)
except:
    pass

Driver.find_element(By.XPATH , "//span[@aria-current='date']").click()
time.sleep(0.5)

Driver.find_element(By.XPATH , "//button[contains(text(),'Apply Filter')]").click()
WebDriverWait(Driver, 30).until(
    EC.presence_of_element_located((By.XPATH , "//tr[@class='table__row  mb-2 mb-md-0']") )
    )
time.sleep(3)
OrdersPage = BeautifulSoup(Driver.page_source , "html.parser")
OrderTRs = Driver.find_elements(By.XPATH , "//tr[@class='table__row  mb-2 mb-md-0']")
JewsonsOrderNumbers = []
JewsonsURLs = []
JewsonsExpenses = []
JewsonsDates = []
OrdersPage = BeautifulSoup(Driver.page_source , "html.parser")
for i in range(len(OrderTRs)):                                    
    OrderHREF = OrdersPage.findAll("a" , href=True , attrs = {"class" : "table__cell-link table__cell-link--order"})[i]["href"]
    OrderHREF = r"https://www.jewson.co.uk/my-account/orders/" + OrderHREF
    OrderInstanceDriver.get(OrderHREF)
    OrderPage = BeautifulSoup(OrderInstanceDriver.page_source , "html.parser")
    OrderNumber = OrderPage.find("div" , attrs={"class" : "pull-sm-right h2 m-0"}).text
    OrderDate = OrderPage.find("dd" , attrs={"class" : "float-right" , "data-section" : "order-date"}).text
    OrderDate = datetime.datetime.strptime(OrderDate , "%d/%m/%Y")
    OrderStatus = OrderPage.find("dd" , attrs={"class" : "float-right" , "data-section" : "order-status"}).text
    OrderExpense = OrderPage.find("dd" , attrs={"class" : "float-right" , "data-section" : "order-total"}).text
    OrderExpense = OrderExpense.replace("£incVAT " , "")
    JewsonsOrderNumbers.append(OrderNumber)
    JewsonsURLs.append(OrderHREF)
    JewsonsExpenses.append(OrderExpense)
    JewsonsDates.append(OrderDate)


SendData = {
          "Jewsons Order Number": JewsonsOrderNumbers,
          "Jewsons URL": JewsonsURLs, 
          "Date" : JewsonsDates,
          "Expense" : JewsonsExpenses
        }

df = pd.DataFrame(SendData)

df.to_csv(OutputDir , index = False)           
            

