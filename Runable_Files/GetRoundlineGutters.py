import pandas as pd
from bs4 import BeautifulSoup as BS
from selenium import webdriver
import re
import time
import numpy as np
import os
import random
import string
import sys
from pathlib import Path
ScriptDir = Path(__file__).parent
OutputDir = ScriptDir.parent / "Outputs"
OutputDir.mkdir(exist_ok=True)
OutputDir = OutputDir / "RoundlineGutters.csv"

sys.path.append(str(Path(__file__).resolve().parent.parent))
from Custom_Functions import UniversalOptionsLoad, MainDriverLoad

UniversalOptionsLoad()
driver = MainDriverLoad()

def GetSoup(url , SleepTime):
  driver.get(url)
  time.sleep(SleepTime)
  driver.set_window_position(-2000,0) # HASH TO SEE LOADED PAGES
  page_source = driver.page_source
  soup = BS(page_source, "html.parser")
  return soup

def TravisPerkinsGetProductDescAndName(TempHTML):
  global AllData
  soup = BS(TempHTML, "html.parser")
    
  Father = soup.findAll("div" , attrs = {"data-test-id" : "plp-list" , "class" : re.compile("styled__GridList")})
  Father = BS(str(Father) , "html.parser")
    
  Prices = Father.findAll("div" , class_  = [re.compile("ProductPrice__PriceUnavailableText") , re.compile("TradePriceBlock__MainPrice")] )
  Names = Father.findAll("span" ,attrs={"color" : "text-default" , "data-test-id" : "product-card-title"})
  Hrefs = Father.findAll("a" , href=True , attrs={"data-test-id" : re.compile("product-card-image") or re.compile("ToolHireProductItemStyled__ImageLinkWrapper")})
  for i in range(len(Hrefs)):
    CurrentProductSurcharge = ""
    CurrentProductVisibility = "FALSE"
    CurrentProductHref = r"https://www.travisperkins.co.uk" + Hrefs[i]["href"]
    
    CurrentProductPrice = Prices[i].text
    CurrentProductPrice = CurrentProductPrice.split("£")
    CurrentProductPrice = CurrentProductPrice[1]
    CurrentProductPrice = CurrentProductPrice.split (" ")
    CurrentProductPrice = CurrentProductPrice[0]
    CurrentProductPrice = float(CurrentProductPrice)
    
    
    NameHalves = Names[i].text
    if "-" in NameHalves:
      NameHalves = NameHalves.split("-")
    else:
      NameHalves = NameHalves.split("(")
    CurrentProductName = NameHalves[0]
    
    Flag = True
    SecondsForSleep = 0.5
    while Flag == True and SecondsForSleep < 7:
      PageHTML = GetSoup(CurrentProductHref , SecondsForSleep)                              
      CurrentProductImage = PageHTML.find_all("img" , class_ = re.compile("Image-q9id2n-1 hQrpPd") )
      try:
        CurrentProductImage = r"https:" + CurrentProductImage[0]["src"]
        Flag = False
      except:
        SecondsForSleep = SecondsForSleep + 2
        
    Description = PageHTML.findAll("li" , class_ = re.compile("ProductOverviewDesktop__ListItem-sc-1cd37aw-1 kcznde"))
    Father = BS(str(Description) , "html.parser")          
    Description = Father.findAll("span" , class_ = re.compile("sc-aXZVg sc-kAyceB gUauWZ jTBDpQ"))
    CurrentProductDescription = ""
    for Desc in Description:
      if CurrentProductDescription != "":
        CurrentProductDescription = CurrentProductDescription + "\n" + Desc.text
      else:
        CurrentProductDescription = CurrentProductDescription + Desc.text
    CurrentProductDescription = CurrentProductDescription.replace("\n" , " <br>")  
    
    TechSpecTable = PageHTML.find("div" , attrs={"data-test-id" : "table" , "class" : "ProductTSDesktop__Table-sc-1il6kg3-1 hVNhLx"})
    Father = BS(str(TechSpecTable) , "html.parser")
    
    IDLength = 20
    characters = string.ascii_letters + string.digits
    handleId = ''.join(random.choice(characters) for _ in range(IDLength))
    handleId = "product_" + handleId
    
    collection = "Squareline Gutter & Fittings"
    Appender = pd.DataFrame({ "handleId" : handleId , "fieldType" : "Product" , "name" : CurrentProductName , "description" : CurrentProductDescription, "productImageUrl" : CurrentProductImage , "collection" : collection , "sku" : "" , "ribbon" : "" , "price" : CurrentProductPrice , 
                             "surcharge" : CurrentProductSurcharge , "visible" : CurrentProductVisibility} , index=[0]) 
    AllData = AllData._append(Appender , ignore_index = True)
    

AllData = pd.DataFrame(columns = ["handleId" , "fieldType" , 	"name" , 	"description"	, "productImageUrl" ,	"collection" ,	"sku" , "ribbon" , "price" , "surcharge" , "visible"]) 

# Insert page for roundline gutters+fixings. 
FullHTML = ""

TravisPerkinsGetProductDescAndName(FullHTML)


os.system("cls")
os.system("cls") 
AllData.to_csv(OutputDir , encoding="cp1252")


