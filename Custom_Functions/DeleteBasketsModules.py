from bs4 import * 
from selenium.webdriver.common.by import By
import time

def DeleteWickesBasket(MainDriver):
    MainDriver.get(r"https://www.wickes.co.uk/cart")
    time.sleep(5)
    try:
        while (True):
            try:
                MainDriver.find_elements(By.XPATH, "//button[@class='btn order-item__remove']")[0].click()
                time.sleep(5)
            except:
                MainDriver.find_elements(By.XPATH, "//button[@class='btn order-item__remove']")[1].click()
                time.sleep(5)
    except:
        pass