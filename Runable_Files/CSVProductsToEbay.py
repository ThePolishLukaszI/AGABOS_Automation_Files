""" UNTESTED SCRIPT: Please monitor what this script does closely.

    """
import pandas as pd
import numpy 
from bs4 import * 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import sys
from pathlib import Path
ScriptDir = Path(__file__).parent
InputDir = ScriptDir.parent / "InputDir"
InputDir.mkdir(exist_ok=True)
InputDir = InputDir / "ProductsToEbay.csv"

sys.path.append(str(Path(__file__).resolve().parent.parent))
from Custom_Functions import *

UniversalOptionsLoad()
driver = MainDriverLoad()

MainDriver = MainDriverLoad()
MainWait = WebDriverWait(MainDriver, 60)


ColumnOutline = pd.DataFrame(columns = ["WixProductName" , "Description" , "SKU" , "Price" , "TechSpec" , "Brand"]) 
column_names = ColumnOutline.columns.tolist()
df = pd.read_csv(
    InputDir,
    names=column_names,
    header=None
)

TopText = r"""<div style="color:rgb(0, 0, 0); font-style:normal; font-variant-ligatures:normal; font-variant-caps:normal; font-weight:400; letter-spacing:normal; orphans:2; text-align:center; text-indent:0px; text-transform:none; word-spacing:0px; white-space:normal; background-color:rgb(255, 255, 255); text-decoration-style:initial; text-decoration-color:initial;"><font color="#7f160e" style="" face="Times New Roman" size="6"><strong style="">Shop Direct at AGABOS.CO.UK</strong></font></div><div style="color:rgb(0, 0, 0); font-style:normal; font-variant-ligatures:normal; font-variant-caps:normal; font-weight:400; letter-spacing:normal; orphans:2; text-align:center; text-indent:0px; text-transform:none; word-spacing:0px; white-space:normal; background-color:rgb(255, 255, 255); text-decoration-style:initial; text-decoration-color:initial;"><font color="#7f160e" face="Times New Roman" size="6"><strong style="">Free Delivery &amp; Better Prices Guaranteed</strong></font></div><div style="color:rgb(0, 0, 0); font-style:normal; font-variant-ligatures:normal; font-variant-caps:normal; font-weight:400; letter-spacing:normal; orphans:2; text-align:center; text-indent:0px; text-transform:none; word-spacing:0px; white-space:normal; background-color:rgb(255, 255, 255); text-decoration-style:initial; text-decoration-color:initial;"><br></div>
"""

BottomText = r"""<div style="color:rgb(0, 0, 0); font-style:normal; font-variant-ligatures:normal; font-variant-caps:normal; font-weight:400; letter-spacing:normal; orphans:2; text-align:center; text-indent:0px; text-transform:none; word-spacing:0px; white-space:normal; background-color:rgb(255, 255, 255); text-decoration-style:initial; text-decoration-color:initial;"><span style="font-family: &quot;Times New Roman&quot;; font-size: large; text-align: start;">All products are sourced through a network of trusted British suppliers.</span></div><div style="color:rgb(0, 0, 0); font-style:normal; font-variant-ligatures:normal; font-variant-caps:normal; letter-spacing:normal; orphans:2; text-align:center; text-indent:0px; text-transform:none; word-spacing:0px; white-space:normal; background-color:rgb(255, 255, 255); text-decoration-style:initial; text-decoration-color:initial;"><font color="#7f160e" style=""><div style="color:rgb(0, 0, 0); font-style:normal; font-variant-ligatures:normal; font-variant-caps:normal; letter-spacing:normal; orphans:2; text-align:start; text-indent:0px; text-transform:none; word-spacing:0px; white-space:normal; text-decoration-style:initial; text-decoration-color:initial;"><div style="text-align:center;"><div style="text-align:start;"><ul style=""><li style=""><font face="Times New Roman" size="4">Delivery is completed within 2–3 working days.</font></li><li style=""><font style="" face="Times New Roman" size="4">Product is brand new, but it may have some minor scratches from movement or handling in the warehouse. These are purely cosmetic and do not affect the item’s functionality.</font></li></ul><p style="font-weight:bold;"></p></div></div><div style="font-weight:400;"><b><b><b><b><b><strong><font color="#5d6f34" face="Times New Roman" size="6"><i style=""><br></i></font></strong></b></b></b></b></b></div></div><div style="font-weight:400; color:rgb(0, 0, 0); font-style:normal; font-variant-ligatures:normal; font-variant-caps:normal; letter-spacing:normal; orphans:2; text-indent:0px; text-transform:none; word-spacing:0px; white-space:normal; text-decoration-style:initial; text-decoration-color:initial; text-align:center;"><div style=""><b><b><b><font color="#7f160e" face="Times New Roman" size="6"><strong>Shop Direct at AGABOS.CO.UK</strong></font></b></b></b></div><div style=""><b style=""><b style=""><b style=""><font color="#7f160e" style=""><strong style=""><font face="Times New Roman" style="" size="6">Free Delivery &amp; Better Prices Guaranteed</font><br></strong></font></b></b></b></div></div></font></div>
"""
input("Press enter when logged in")
for index, Product in df.iterrows():
    if Product["WixProductName"] == "name":
        continue
    MainDriver.get(r"https://www.ebay.co.uk/sl/prelist/identify?")
    EnterElement(MainDriver , "//input[@id='s0-1-1-24-10-@prelist-radix-body-2-20-@side-pane-1-@dialog-16-1-5-2-5-10-14-@input-textbox']" , "Gutter C")
    ClickElement(MainDriver , "//input[@id='s0-1-1-24-10-@prelist-radix-body-2-20-@side-pane-1-@dialog-16-1-5-2-5-10-18-categoryId-259232']")
    try:
        MainDriver.find_element(By.XPATH , "//button[@id='gdpr-banner-accept']").click()
    except:
        pass
    ClickElement(MainDriver , "//button[@class='textual-display btn btn--secondary prelist-radix__next-action']")
    ClickElement(MainDriver , "//input")    
    ClickElement(MainDriver , "//button[@class='textual-display btn btn--primary condition-dialog-radix__continue-btn']")
    
    EnterElement(MainDriver , "//input" , Product["WixProductName"])
    
    ClickElement(MainDriver , "//button[@name='attributes.Colour']")
    EnterElement(MainDriver , "//input[@name='search-box-attributesColour']" , "Black")
    EnterElement(MainDriver , "//input[@name='search-box-attributesColour']" , Keys.ENTER)
    
    ClickElement(MainDriver , "//button[@name='attributes.Brand']")
    ClickElement(MainDriver , "//input[@name='search-box-attributesBrand']" , Product["Brand"])
    EnterElement(MainDriver , "//input[@name='search-box-attributesBrand']" , Keys.ENTER)
    
    ClickElement(MainDriver , "//input[@class='feature--editHtml']")
    EnterElement(MainDriver , "//div[@data-ghosttext='Write a detailed description of your item, or save time and let AI draft it for you.']" , TopText)
    EnterElement(MainDriver , "//div[@data-ghosttext='Write a detailed description of your item, or save time and let AI draft it for you.']" , Product["Description"])
    EnterElement(MainDriver , "//div[@data-ghosttext='Write a detailed description of your item, or save time and let AI draft it for you.']" , BottomText)
    ClickElement(MainDriver , "//input[@class='feature--editHtml']")
    
    input("Enter Image and check desc")
    EnterElement(MainDriver , "//input[@name='price']" , Product["Price"])
    ClickElement(MainDriver , "(//button[@class='toggle-button toggle-button--gallery-layout'])[2]")
    
    ClickElement(MainDriver , "//div[@class='textual-display se-field-card__content-description']")
    ClickElement(MainDriver , "//input[@id='c2-1-24-1-25[1]-24-1-25[7]-35-1-2-0-@gqlc-0-4-2-10-3-0-12-0-0-@dialog-16-1-3-0-1[1]-6-2[1]-6[0[1]]-managedShippingPackageSize']")
    ClickElement(MainDriver , "(//button[@class='btn btn--primary'])[3]")

    input("Double check listing")
    ClickElement(MainDriver , "//button[@data-key='listItCallToAction']")
    
    