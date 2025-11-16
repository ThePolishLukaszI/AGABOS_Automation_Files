import pandas as pd
from bs4 import BeautifulSoup as BS
import re
import time
import numpy as np
import os
import sys
from pathlib import Path
ScriptDir = Path(__file__).parent
OutputDir = ScriptDir.parent / "Outputs"
OutputDir.mkdir(exist_ok=True)
OutputDir = OutputDir / "FacingBricks.csv"

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
  global AllData , CurrentProductID, Colours
  soup = BS(TempHTML, "html.parser")
    
  Father = soup.findAll("div" , attrs = {"data-test-id" : "plp-list" , "class" : re.compile("styled__GridList")})
  Father = BS(str(Father) , "html.parser")
    
  Prices = Father.findAll("div" , class_  = [re.compile("ProductPrice__PriceUnavailableText") , re.compile("TradePriceBlock__MainPrice")] )
  Names = Father.findAll("span" ,attrs={"color" : "text-default" , "data-test-id" : "product-card-title"})
  Hrefs = Father.findAll("a" , href=True , attrs={"data-test-id" : re.compile("product-card-image") or re.compile("ToolHireProductItemStyled__ImageLinkWrapper")})
  for i in range(len(Hrefs)):
    ProductType = "NOT FOUND"
    CurrentProductPrice = Prices[i].text
    CurrentProductHref = r"https://www.travisperkins.co.uk" + Hrefs[i]["href"]
    
    NameHalves = Names[i].text # Remove unneccssary fluff from name
    if "(" in NameHalves:
      NameHalves = NameHalves.split("(")
    elif "-" in NameHalves:
      NameHalves = NameHalves.split("-")
    elif "Pack" in NameHalves:
      NameHalves = NameHalves.split("Pack")
    elif "pack" in NameHalves:
      NameHalves = NameHalves.split("pack")
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
        
    DescPoints = PageHTML.findAll("li" , class_ = re.compile("ProductOverviewDesktop__ListItem-sc-1cd37aw-1 kcznde"))
    Father = BS(str(DescPoints) , "html.parser")
    DescPoints = Father.findAll("span" , class_ = re.compile("sc-aXZVg sc-kAyceB gUauWZ jTBDpQ"))
    CurrentProductPoints = ""
    for Desc in DescPoints:
      if CurrentProductPoints != "":
        CurrentProductPoints = CurrentProductPoints + "\n" + Desc.text
      else:
        CurrentProductPoints = CurrentProductPoints + Desc.text
    
    TechPoints = PageHTML.find("div" , attrs={"data-test-id" : "table" , "class" : "ProductTSDesktop__Table-sc-1il6kg3-1 hVNhLx"})
    Father = BS(str(TechPoints) , "html.parser")
    TechPoints = Father.findAll("span" , attrs={"class" : "sc-aXZVg sc-kAyceB gUauWZ jTBDpQ" , "color" : "text-default"})
    for Point in TechPoints:
      Attr = Point.text.lower()
      if Attr in Colours or Attr == "buff":
        ProductType = Attr
        break
    
    if ProductType == "NOT FOUND":
      for Point in TechPoints:
        Attr = Point.text.lower()
        if Attr in ColoursExtended: # If colour isn't yet found, try to find it in the tech spec
          ProductType = Attr
          break
      if ProductType != "NOT FOUND":
        for i in range(len(ColoursExtended)):
          if ColoursExtended[i] == ProductType: #Filter colour families into colour names... reds into red, yellows into yellow and so on.
            ProductType = Colours[i]
    
    if ProductType == "NOT FOUND":
      ProductType = "Uncategorised"
    ProductType = ProductType.capitalize()
    
    
    CurrentProductHeight = ""
    TechSpecTable = PageHTML.find("div" , attrs={"data-test-id" : "table" , "class" : "ProductTSDesktop__Table-sc-1il6kg3-1 hVNhLx"})
    Father = BS(str(TechSpecTable) , "html.parser")
    Tables = Father.findAll(attrs = {"class" : "ProductTSDesktop__Property-sc-1il6kg3-2 djfjTt"})
    for b in range(len(Tables)):
      if "height" in Tables[b].text or "Height" in Tables[b].text:
        Father = BS(str(Tables[b]) , "html.parser")
        Text = Father.find("span" , attrs = {"color" : "text-default"})
        CurrentProductHeight= Text.text
        break
    if CurrentProductHeight == "":
      CurrentProductHeight = "Unkown"
    
    TempID = ""
    CurrentProductID = CurrentProductID + 1
    if CurrentProductID >=100:
      TempID = str(CurrentProductID)
    elif CurrentProductID < 100 and CurrentProductID >= 10:
      TempID = "0" + str(CurrentProductID)
    elif CurrentProductID < 10:
      TempID = "00" + str(CurrentProductID)
    else:
      TempID = str(CurrentProductID)      
      
    Appender = pd.DataFrame({"Product Name" : CurrentProductName , "Image" : CurrentProductImage , "Height" : CurrentProductHeight,  "Other Description" : CurrentProductPoints, "ID" : ("BR" + str(TempID)), "Url/Href" : CurrentProductHref , "TP Price" : CurrentProductPrice , "Brick Type" : ProductType} , index=[0]) 
    AllData = AllData._append(Appender , ignore_index = True)
    
  
AllData = pd.DataFrame(columns = ["Product Name" , "Image" , "Height" ,  "Other Description" , "ID" , "Url/Href" , "TP Price" , "Brick Type"]) 
CurrentProductID = 0
Colours = ["red" , "yellow" , "brown" , "grey" , "orange" , "blue"]
ColoursExtended = ["reds" , "yellows" , "browns" , "greys" , "oranges" , "blues"]

# Insert page for facing bricks. 
FullHTML = ""

TravisPerkinsGetProductDescAndName(FullHTML)

os.system("cls")
os.system("cls") 
AllData.to_csv(OutputDir , encoding="cp1252")


