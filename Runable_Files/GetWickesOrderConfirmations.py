import pandas as pd
import numpy 
from bs4 import * 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import sys
from pathlib import Path
ScriptDir = Path(__file__).parent
OutputDir = ScriptDir.parent / "Outputs"
OutputDir.mkdir(exist_ok=True)
OutputDir = OutputDir / "WickesOrderConfirmations"
OutputDir.mkdir(exist_ok=True)

sys.path.append(str(Path(__file__).resolve().parent.parent))
from Custom_Functions import *

UniversalOptionsLoad()
MainDriver = MainDriverLoad()
MainWait = WebDriverWait(MainDriver, 60)

os.chdir(OutputDir)

MainDriver.get("https://mail.google.com/mail/u/1/#advanced-search/from=noreply%40wickes.co.uk&query=%22order+confirmation%22&isrefinement=true&fromdisplay=noreply%40wickes.co.uk")
OrderDone = []
def MainLoop():
    MainWait.until(EC.element_to_be_clickable((By.XPATH , "(//tbody)[last()]/tr/td[5]/div/div/div[2]/span" )))
    for i in range(len(MainDriver.find_elements(By.XPATH , "(//tbody)[last()]/tr/td[5]/div/div/div[2]/span"))):
        Tag = GetElement(MainDriver , f"((//tbody)[last()]/tr/td[5]/div/div/div[2]/span)[{i+1}]" , ShouldScroll=True)
        original_window = MainDriver.current_window_handle
        Text = Tag.text
        Order = Text.split("on " , 1)[1]
        if Order in OrderDone: 
            pass
        OrderDone.append(Order)
        actions = ActionChains(MainDriver)
        actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).click(Tag).key_up(Keys.CONTROL).key_up(Keys.SHIFT).perform()
        time.sleep(1)
        NewWindow = MainDriver.window_handles[-1]
        MainDriver.switch_to.window(NewWindow)
        time.sleep(1)
        Element = GetElement(MainDriver , "(//a[contains(@href,'https://mail.google.com/mail/u/')])[last()]" , ShouldScroll=True)
        actions = ActionChains(MainDriver)
        actions.move_to_element(Element).perform()
        time.sleep(1)
        ClickElement(MainDriver , "(//a[contains(@href,'https://mail.google.com/mail/u/')])[last()]/../div/span/button/div")
        time.sleep(1)
        MainDriver.close()
        MainDriver.switch_to.window(original_window)
        time.sleep(1)

while True:
    MainLoop()
    Past = MainDriver.current_url
    ClickElement(MainDriver , "(//div[@aria-label='Show more messages'])/../div[3]")
    New = MainDriver.current_url
    if New==Past:
        print("Check")
    print("Click!")
