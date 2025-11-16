""" Functions designed to keep code simpler and easier to write. Some scripts use builtin functions however (where possible) use these instead"""
from bs4 import * 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re
import time

def HoverElement(LocalDriver , LocalXPATH):
    Wait = WebDriverWait(LocalDriver, 2)
    element_to_hover_over =  Wait.until(EC.visibility_of_element_located((By.XPATH , LocalXPATH)))  
    hover = ActionChains(LocalDriver).move_to_element(element_to_hover_over)
    hover.perform()
    
def SelectElement(LocalDriver, LocalXPATH , Text , ShouldScroll=False , Mode="Default"):
    Wait = WebDriverWait(LocalDriver, 999)
    Element = Wait.until(EC.presence_of_element_located((By.XPATH , LocalXPATH)))
    if Mode.lower() == "compatability":
        if ShouldScroll:
            LocalDriver.execute_script("arguments[0].scrollIntoView();", Element)
            time.sleep(0.5)
        if isinstance(Text ,  type(re.compile(""))):
           script = f'''
                var select = arguments[0];
                var regex = new RegExp("{Text}", "i"); // Case-insensitive regex
                for (var i = 0; i < select.options.length; i++) {{
                    if (regex.test(select.options[i].text)) {{
                        select.options[i].selected = true;
                        break; }}}}  select.dispatchEvent(new Event('change'));  '''
        else: 
            script = f'''
                var select = arguments[0];
                for (var i = 0; i < select.options.length; i++) {{
                    if (select.options[i].text === "{Text}") {{
                        select.options[i].selected = true;
                        break; }}}}  select.dispatchEvent(new Event('change'));  '''
        LocalDriver.execute_script(script, Element)
        return
    
    if Mode.lower() == "iterate":
        Elements = Wait.until(EC.visibility_of_any_elements_located((By.XPATH , LocalXPATH)))
        for Tag in Elements:
            if Tag.is_displayed():
                Element=Tag
                break
    else:
        Element = Wait.until(EC.visibility_of_element_located((By.XPATH , LocalXPATH)))  
    if ShouldScroll:
        LocalDriver.execute_script("arguments[0].scrollIntoView();", Element)
        time.sleep(0.5) 
        
    #if Mode.lower() == "default"
    Dropdown = Select(Element)  
    if isinstance(Text ,  type(re.compile(""))):
        for Option in Dropdown.options:
            if Text.search(Option.text):
                Dropdown.select_by_visible_text(Option.text)
                break

def GetElement(LocalDriver, LocalXPATH , ShouldScroll=False , Mode="Default"):
    Wait = WebDriverWait(LocalDriver, 60)
    Element = Wait.until(EC.presence_of_element_located((By.XPATH , LocalXPATH)))
    if Mode.lower() == "compatability":
        if ShouldScroll:
            LocalDriver.execute_script("arguments[0].scrollIntoView();", Element)
            time.sleep(0.5)
        return Element
    
    if Mode.lower() == "iterate":
        Elements = Wait.until(EC.visibility_of_any_elements_located((By.XPATH , LocalXPATH)))
        for Tag in Elements:
            if Tag.is_displayed():
                Element=Tag
                break
    else:
        Element = Wait.until(EC.visibility_of_element_located((By.XPATH , LocalXPATH)))  
    if ShouldScroll:
        LocalDriver.execute_script("arguments[0].scrollIntoView();", Element)
        time.sleep(0.5) 
    Wait.until(EC.element_to_be_clickable(Element))
    return Element

def ClickElement(LocalDriver, LocalXPATH , ShouldScroll=False , Mode="Default"):
    Wait = WebDriverWait(LocalDriver, 30)
    Element = Wait.until(EC.presence_of_element_located((By.XPATH , LocalXPATH)))
    if Mode.lower() == "compatability":
        if ShouldScroll:
            LocalDriver.execute_script("arguments[0].scrollIntoView();", Element)
            time.sleep(0.5)
        LocalDriver.execute_script("arguments[0].click();", Element)
        return
    
    if Mode.lower() == "iterate":
        Elements = Wait.until(EC.visibility_of_any_elements_located((By.XPATH , LocalXPATH)))
        for Tag in Elements:
            if Tag.is_displayed():
                Element=Tag
                break
    if ShouldScroll:
        LocalDriver.execute_script("arguments[0].scrollIntoView();", Element)
        time.sleep(0.5) 
    Element.click()

def EnterElement(LocalDriver, LocalXPATH , Text , ShouldScroll=False , Mode="Default"):
    Wait = WebDriverWait(LocalDriver, 60)
    Element = Wait.until(EC.presence_of_element_located((By.XPATH , LocalXPATH)))
    if Mode.lower() == "compatability":
        if ShouldScroll:
            LocalDriver.execute_script("arguments[0].scrollIntoView();", Element)
            time.sleep(0.5)
        LocalDriver.execute_script("arguments[0].value = arguments[1];", Element , Text)
        return
    
    if Mode.lower() == "iterate":
        Elements = Wait.until(EC.visibility_of_any_elements_located((By.XPATH , LocalXPATH)))
        for Tag in Elements:
            if Tag.is_displayed():
                Element=Tag
                break
    else:
        Element = Wait.until(EC.visibility_of_element_located((By.XPATH , LocalXPATH)))  
    if ShouldScroll:
        LocalDriver.execute_script("arguments[0].scrollIntoView();", Element)
        time.sleep(0.5) 
    Wait.until(EC.element_to_be_clickable(Element))
    Element.send_keys(Text) 
