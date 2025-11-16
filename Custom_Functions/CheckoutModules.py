from bs4 import * 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from pathlib import Path
ScriptDir = Path(__file__).parent
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

def WickesCheckout(MainDriver):
    MainDriver.find_element(By.XPATH, "//input[@id='card_nameOnCard']").clear()
    MainDriver.find_element(By.XPATH, "//input[@id='card_nameOnCard']").send_keys("lukasz pawel ilnicki")
    MainDriver.find_element(By.XPATH, "//input[@id='card_nameOnCard']").clear()
    MainDriver.find_element(By.XPATH, "//input[@id='card_nameOnCard']").send_keys("lukasz pawel ilnicki")
    MainDriver.find_element(By.XPATH, "//input[@id='address-lookup-query']").send_keys(RegisteredAddress)
    time.sleep(1)
    MainDriver.find_element(By.XPATH , "//li[@role='option']").click()
    time.sleep(1)
    MainDriver.find_element(By.XPATH , "//button[@form='hopPaymentAddressPostForm']").click()
    time.sleep(5)

    MainDriver.switch_to.frame("hopIframe")  # Replace with actual iframe ID
    MainDriver.find_element(By.XPATH, "//input[@id='cardNumber']").clear() 
    MainDriver.find_element(By.XPATH, "//input[@id='cardNumber']").send_keys(CardNumber)
    time.sleep(1)
    MainDriver.find_element(By.XPATH, "//input[@id='csc']").send_keys(CVC)
    dropdown = Select(MainDriver.find_element(By.ID, "expiryMonth"))  
    time.sleep(1)
    dropdown.select_by_visible_text(ExpiryMonth)

    dropdown = Select(MainDriver.find_element(By.ID, "expiryYear"))  
    time.sleep(1)
    dropdown.select_by_visible_text(ExpiryYear)
    time.sleep(1)
    MainDriver.find_element(By.XPATH , "//div[@id='paynowButtonHolder']").click()
    print("Confirm payment")
    WebDriverWait(MainDriver, 999).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='header__order-number']"))
    )