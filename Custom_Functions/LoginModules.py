from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import sys
from pathlib import Path
ScriptDir = Path(__file__).parent
InfoDir = ScriptDir.parent / "SensitiveInfo.txt"
Variables = {}
for line in InfoDir.read_text().splitlines():
    key, value = line.split("=")
    Variables[key.strip()] = value.strip()
CardNumber = Variables["CardNumber"]
CVC = Variables["cvc"]

def WickesLogin(MainDriver):
    WickesLoginEmail = Variables["WickesLoginEmail"]
    WickesLoginPassword = Variables["WickesLoginPassword"]
    MainDriver.get(r"https://www.wickes.co.uk/login")
    try:
        WebDriverWait(MainDriver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ("[class='btn btn-primary g-recaptcha']") ))
            )
        try:
            EmailInput = MainDriver.find_element(By.CSS_SELECTOR , ("[id='j_username']") ).clear()
            for i in range(150):
                EmailInput.send_keys(Keys.BACKSPACE)
            EmailInput.send_keys(WickesLoginEmail)
        except:
            pass
        
        try:
            PasswordInput = MainDriver.find_element(By.CSS_SELECTOR , ("[id='j_password']") )
            for i in range(150):
                PasswordInput.send_keys(Keys.BACKSPACE)
            MainDriver.find_element(By.CSS_SELECTOR , ("[id='j_password']") ).send_keys(WickesLoginPassword)
        except:
            pass
        
        MainDriver.find_element(By.CSS_SELECTOR, ("[class='btn btn-primary g-recaptcha']") ).click()
        time.sleep(2)
    except:
        input("Enter when logged in")
        

def TravisPerkinsLogin(MainDriver):
    TravisPerkinsEmail = Variables["TravisPerkinsEmail"]
    TravisPerkinsPassword = Variables["TravisPerkinsPassword"]
    MainDriver.get(r"https://www.travisperkins.co.uk/login")
    try:
        WebDriverWait(MainDriver, 5).until(
            EC.presence_of_element_located((By.XPATH , "//iframe[@data-test-id='oauth-iframe']") )
            )
        MainDriver.switch_to.frame(MainDriver.find_element(By.XPATH , "//iframe[@data-test-id='oauth-iframe']"))
        MainDriver.find_element(By.XPATH , "//input[@id='username']").send_keys(TravisPerkinsEmail)
        MainDriver.find_element(By.XPATH , "//input[@id='password']").send_keys(TravisPerkinsPassword)
    except:
       pass
    
    try:
        MainDriver.find_element(By.XPATH , "//div[@class='checkbox-icon-wrap']").click()
    except:
        pass
    
    try:
        MainDriver.find_element(By.XPATH , "//input[@type='submit']").click()
    except:
        pass
    
    
def JewsonsLogin(MainDriver):
    JewsonsEmail = Variables["JewsonsEmail"]
    JewsonsPassword = Variables["JewsonsPassword"]
    MainDriver.get(r"https://www.jewson.co.uk/login")
    WebDriverWait(MainDriver, 5).until(
            EC.presence_of_element_located((By.XPATH , "//input[@id='okta-signin-username']") )
            )
    
    try:
        EmailInput = MainDriver.find_element(By.CSS_SELECTOR , ("[id='okta-signin-username']") )
        for i in range(150):
            EmailInput.send_keys(Keys.BACKSPACE)
        EmailInput.send_keys(JewsonsEmail)
    except:
        pass
    
    try:
        PasswordInput = MainDriver.find_element(By.CSS_SELECTOR , ("[id='okta-signin-password']") )
        for i in range(150):
            PasswordInput.send_keys(Keys.BACKSPACE)
        MainDriver.find_element(By.CSS_SELECTOR , ("[id='okta-signin-password']") ).send_keys(JewsonsPassword)
    except:
        pass
    time.sleep(1)
    try:
        MainDriver.find_element(By.XPATH, "//input[@class='button button-primary']" ).click()
    except:
        input("ACCEPT COOKIE")
        MainDriver.find_element(By.XPATH, "//input[@class='button button-primary']" ).click()
    time.sleep(2)
