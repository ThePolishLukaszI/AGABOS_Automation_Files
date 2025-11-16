""" PLEASE NOTE: This is a rough draft script that ended up only being used once.
        It is kept incase it ever proves to be useful in the future. 
        
        """

import pandas as pd
from bs4 import BeautifulSoup as BS
from selenium import webdriver
import re
import time
import numpy as np
import os
from pathlib import Path
ScriptDir = Path(__file__).parent
OutputDir = ScriptDir.parent / "Outputs"
OutputDir.mkdir(exist_ok=True)
OutputDir = OutputDir / "100iFoundation.csv"

pd.set_option('display.max_colwidth', None)
pd.reset_option('display.max_colwidth', None)
driver = webdriver.Chrome()
options = webdriver.ChromeOptions() 
options.add_argument("start-minimized")
options.add_argument("--ignore-certificate-errors")
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
options.add_argument('--headless')

def GetSoup(url): 
    driver.get(url)
    time.sleep(1)
    driver.set_window_position(-2000,0) # HASH TO SEE LOADED PAGES
    page_source = driver.page_source
    soup = BS(page_source, "html.parser")
    return soup

def AppendTempDataWithCurrentCompanySearch(Names , Prices , Hrefs , Words , CompanyNamePrefix , CompanyNameFull):
    global AllData , Input, TempData, AbsoluteAllData, url, CurrentSizeInput
    for i in range(len(Names)):
        
        Keys = (Names[i].text).split(" ")
        
        ExtraAttrs = ""
        for Key in Keys:
            if "hollow" == Key.lower():
                ExtraAttrs = ExtraAttrs + "Hollow"  
            if Key == "75mm" or Key == "Pack" :
                Superflag = True
                flag = True
        
        if ExtraAttrs != "Hollow" and CurrentSizeInput == "215mm":
            continue
        if CurrentSizeInput not in Keys:
            continue  
        
        IndexOfForce = "CCC"
        IndexOfTypeDensity = "TBD"
        OverrideSize = ""
        Superflag = False
        flag = False
        for b in range(len(Keys)):
            try:
                if (Keys[b][-1] == "N" or Keys[b][-1] == "n"):
                    IndexOfForce = Keys[b]
                    break   
            except:
                pass
        for b in range(len(Keys)):
            if "." in Keys[b] and Input != "Concrete Common".replace(" " , "-").replace("." , "-"):
                IndexOfForce = Keys[b] + "N"
                break  
        for b in range(len(Keys)):
            try:
                if (Keys[b][-1] == "N" or Keys[b][-1] == "n") and "." in Keys[b]:
                    IndexOfForce = Keys[b]
                    break  
            except:
                pass
        if IndexOfForce == "CCC" or IndexOfForce == "Celcon":
            IndexOfForce = "TBD"
        if IndexOfForce == "7N":
            IndexOfForce = "7.3N"
        if Input == "Concrete Common".replace(" " , "-").replace("." , "-") and (IndexOfForce == "Common" or IndexOfForce == ""):
            IndexOfForce = "7.3N"
                    
        for b in range(len(Keys)):
            try:
                if Keys[b+1].lower() == "density":
                    try:
                        if Keys[b-1].lower() == "ultra":
                            IndexOfTypeDensity = "Ultra" + Keys[b]
                        else:
                            IndexOfTypeDensity = Keys[b]
                            break
                    except:
                        IndexOfTypeDensity = Keys[b]
                        break
                if Keys[b].lower() == "dense":
                    try:
                        if Keys[b-1].lower() == "low":
                            IndexOfTypeDensity = Keys[b-1]
                        else:
                            IndexOfTypeDensity = Keys[b]
                    except:   
                        IndexOfTypeDensity = Keys[b]
                    for Key in Keys:
                        if Key.lower() == "medium":
                            IndexOfTypeDensity = "Medium"
                    break
            except:
                pass
        if IndexOfTypeDensity == "TBD":
            if "ultra lightweight" in (Names[i].text).lower() or "ultra-lightweight" in (Names[i].text).lower():
                IndexOfTypeDensity = "Ultra Lightweight"
            if "standard" in (Names[i].text).lower():
                IndexOfTypeDensity = "standard"
            if "hi-strength" in (Names[i].text).lower() or "high strength" in (Names[i].text).lower():
                IndexOfTypeDensity = "High Strength" 
            if "hollow" in (Names[i].text).lower():
                IndexOfTypeDensity = "Hollow"
            if "hi-7" in (Names[i].text).lower() or "Hi-7" in (Names[i].text).lower():
                IndexOfTypeDensity = "Hi-7"
            if "solar" in (Names[i].text).lower():
                IndexOfTypeDensity = "Solar"
        for Key in Keys:
            if Key.lower() == "shield":
                IndexOfTypeDensity = "standard"
                
                
        match IndexOfTypeDensity: ## signals might be
            case "Dense":
                IndexOfTypeDensity = "2000"
            case "High Strength":
                IndexOfTypeDensity = "730" #2000
            case "Medium":
                IndexOfTypeDensity = "1300" #1000
            case "Ultra Lightweight":
                IndexOfTypeDensity = "530" #800
            case "Hi-7":
                IndexOfTypeDensity = "730" #600
            case "standard":
                IndexOfTypeDensity = "2000" #600
            case "UltraLow":
                IndexOfTypeDensity = "530" #530 
            case "Solar":
                IndexOfTypeDensity = "460" #460 
            case "TBD":
                IndexOfTypeDensity = "2000" #to sort errors with aearated bloacks and thermalite shite
                for Key in Keys:
                    if "medium" == Key.lower():
                        IndexOfTypeDensity = "1300"
                    
                 
          
    
        for Word in Words:
            if Word.lower() == "concrete":
                pass
            else:
                if Word.lower() not in (Names[i].text).lower() and Word.replace("m" , "") not in Names[i].text:
                    flag = True
                    Superflag = True
                    break
                if "paving" in (Names[i].text).lower():
                    Superflag = True
                    flag = True
        
        if Input == "Concrete Common".replace(" " , "-").replace("." , "-"):
            for Key in Keys:
                if Key == "Pack":
                    Superflag = True
                    flag = True
                if Key == "65mm" or Key == "(H)65mm":
                    OverrideSize = "CC 65mm"
                    IndexOfTypeDensity = "2000"
                if Key == "73mm" or Key == "(H)73mm": 
                    OverrideSize = " CC 73mm"
                    IndexOfTypeDensity = "2000"
                    #flag = True
                    
        if IndexOfForce == "TBD":
            if IndexOfTypeDensity == "2000":
                IndexOfForce = "7.3N"
            else:
                IndexOfForce = "3.6N"
                
        if IndexOfForce == "7.6NN":
            IndexOfForce = "7.6N"
        if IndexOfForce == "3.6NN":
            IndexOfForce = "3.6N"
            
        if IndexOfForce == "3.6N" and IndexOfTypeDensity == "1300":
            flag = True
        if IndexOfTypeDensity == "Hollow":
            IndexOfTypeDensity = "2000"
        
        try:
            if int(IndexOfTypeDensity) < 1200:
                flag = True  
        except:
            pass
        
        if IndexOfForce == "2.9N" or IndexOfForce == "2.9NN" or IndexOfForce == "22N":
            flag = True
        
        if Input == "foundation block".replace(" " , "-").replace("." , "-") and IndexOfForce == "3.6N":
            continue
        
         #APPEND TO ALL NON REMOVE PRODUCTS
        if Superflag == False:
            ListToRemove = ["Â" , "£" , "p" , "e" , "r" , "a" , "c" , "k" , "h" , " " , "s" , "q" , "u" , "m" , "t" , "," ]
            TempPrice = Prices[i].text
            for char in range(len(ListToRemove)):
                TempPrice = TempPrice.replace(ListToRemove[char] , "")
            try:
                Prices[i] = float(TempPrice)
            except:
                Prices[i] = "Price unavailable"
            AbsoluteAppender = pd.DataFrame({"Product Name" : Names[i].text , "Company" : CompanyNameFull , "Price" : Prices[i] , "Href" : (CompanyNamePrefix + Hrefs[i]["href"]) , "Force" : IndexOfForce , "TypeOfDensity" : IndexOfTypeDensity , "ExtraAttrs" : ExtraAttrs , "Size" : OverrideSize} , index = [0])
            AbsoluteAllData = AbsoluteAllData._append(AbsoluteAppender, ignore_index = True)     
        
        if flag == False:
            ListToRemove = ["Â" , "£" , "p" , "e" , "r" , "a" , "c" , "k" , "h" , " "]
            Prices[i] = float(TempPrice)
            Appender = pd.DataFrame({"Product Name" : Names[i].text , "Company" : CompanyNameFull , "Price" : Prices[i] , "Href" : (CompanyNamePrefix + Hrefs[i]["href"]) , "Force" : IndexOfForce , "TypeOfDensity" : IndexOfTypeDensity , "ExtraAttrs" : ExtraAttrs , "Size" : OverrideSize} , index = [0])
            TempData = TempData._append(Appender, ignore_index = True)
    


#SEARCHED ITEMS  INCLUDES VAT
def TravisPerkinsGetPricesNamesFromSearch(url):
    global AllData , Input, TempData
    soup = GetSoup(url)
    Words = Input.split("-")
    
    Father = soup.findAll("div" , attrs = {"data-test-id" : "plp-list" , "class" : re.compile("styled__GridList")})
    Father = BS(str(Father) , "html.parser")
    
    Prices = Father.findAll(["div"] , class_  = [re.compile("ProductPrice__PriceUnavailableText") , re.compile("TradePriceBlock__MainPrice")] )
    Names = Father.findAll("span" ,attrs={"color" : "text-default" , "data-test-id" : "product-card-title"})
    Hrefs = Father.findAll("a" , href=True , attrs={"class" : re.compile("ProductItemDesktopNewFlow__ProductImage") or re.compile("ToolHireProductItemStyled__ImageLinkWrapper")})

    AppendTempDataWithCurrentCompanySearch(Names , Prices , Hrefs , Words , r"https://www.travisperkins.co.uk" , "Travis Perkins")
      
def JewsonGetPriceNamesFromSearch(url):
    global AllData, Input, TempData
    soup = GetSoup(url)
    Words = Input.split("-")
    
    Father = soup.findAll("div" , attrs= {"class" : re.compile("col-6 col-md-4")})
    Father = BS(str(Father) , "html.parser")
    
    Prices = Father.findAll(["h3" , "span"] , class_ =  [re.compile("price-missing__title") , re.compile("js-price-value")])
    Names = Father.findAll("p" ,attrs={"class" : re.compile("product__name") })
    Hrefs = Father.findAll("a" , href=True , attrs={"class" : re.compile("product__thumb") , "data-event" : re.compile("productClick")})
    
    AppendTempDataWithCurrentCompanySearch(Names , Prices , Hrefs , Words , "" , "Jewson")
                       
def SelcoGetPricesNamesFromSearch(url): 
    global AllData, Input, TempData
    soup = GetSoup(url)
    Words = Input.split("-")
    
    Father = soup.findAll("li" , attrs = {"class" : re.compile("ProductList-item-2ql")})
    Father = BS(str(Father) , "html.parser")

    Names = Father.findAll("a" ,attrs={"class" : re.compile("ProductListItem-link")})
    Hrefs = Father.findAll("a" , href=True , attrs={"class" : re.compile("ProductListItem-link")})
    
    Father = soup.findAll("span" , attrs = {"class" : re.compile("PriceBox-item-3SD PriceBox-itemIncVat")})
    Father = BS(str(Father) , "html.parser")
    Prices = Father.findAll("span" , string = re.compile("£"))
    
    AppendTempDataWithCurrentCompanySearch(Names , Prices , Hrefs , Words , r"https://www.selcobw.com" , "Selco")

def WickesGetPricesNamesFromSearch(url):
    global AllData, Input, TempData
    soup = GetSoup(url)
    Words = Input.split("-")
    
    Father = soup.findAll("div" , attrs = {"class" : re.compile("products-list products-list")})
    Father = BS(str(Father) , "html.parser")

    Names = Father.findAll("a" ,attrs={"class" : re.compile("product-card__title product-card")})
    Hrefs = Father.findAll("a" , href=True , attrs={"class" : re.compile("product-card__title product-card")})
    Prices = Father.findAll("div" , attrs={"class" : re.compile("main-price__value product-card__price-value")})
    
    AppendTempDataWithCurrentCompanySearch(Names , Prices , Hrefs , Words , r"https://www.wickes.co.uk" , "Wickes")

def BnQGetPricesNamesfromSearch(url):
    global AllData, Input, TempData
    soup = GetSoup(url)
    Words = Input.split("-")
    
    Father = soup.findAll("li" , attrs = {"class" : re.compile("max-md:!border-x-0 max-md:!border-t-0 max-md")})
    Father = BS(str(Father) , "html.parser")

    Names = Father.findAll("p" ,attrs={"class" : re.compile("mb-sm font-bold")})
    Hrefs = Father.findAll("a" , href=True , attrs={"data-testid" : re.compile("product-link")})
    Prices = Father.findAll("span" , attrs={"data-testid" : re.compile("product-price")})
    
    AppendTempDataWithCurrentCompanySearch(Names , Prices , Hrefs , Words , r"https://www.diy.com/departments" , "BnQ")

def BMNWGetPricesNamesfromSearch(url):
    global AllData, Input, TempData
    soup = GetSoup(url)
    Words = Input.split("-")
    
    Father = soup.findAll("div" , attrs = {"class" : re.compile("blm-product-search-details-container")})
    Father = BS(str(Father) , "html.parser")
    Names = Father.findAll("a" ,attrs={"class" : "blm-product-search-details-container__title null dyMonitor"})
    Hrefs = Father.findAll("a" , href=True , attrs={"class" : re.compile("null dyMonitor")})
    
    Father = soup.findAll("div" , attrs = {"class" : re.compile("blm-product-search-details-container__price active")})
    Father = BS(str(Father) , "html.parser")
    Prices = Father.findAll("span" , attrs={"class" : "blm-product-search-details-container__final-price price-inc-vat"})
    
    AppendTempDataWithCurrentCompanySearch(Names , Prices , Hrefs , Words , r"" , "BMNW")
    
    
    
#CREATE SEARCH FOR INPUT
def TravisPerkinsCreateSearch(Text):
    Text = "".join(["https://www.travisperkins.co.uk/search/?text=" , Text])
    return Text

def JewsonsCreateSearch(Text):
    Text = "".join(["https://www.jewson.co.uk/search?text=" , Text])
    return Text

def SelcoCreateSearch(Text):
    Text = "".join(["https://www.selcobw.com/catalogsearch/results/shop-by/q/" , Text])
    return Text
    
def WickesCreateSearch(Text):
    Text = "".join(["https://www.wickes.co.uk/search?text=" , Text])
    return Text

def BnQCreateSearch(Text):
    Text = "".join(["https://www.diy.com/search?term=" , Text])
    return Text

def BMNWCreateSearch(Text):
    Text = "".join(["https://www.buildingmaterials.co.uk/catalogsearch/result/?q=" , Text])
    return Text


def CondenseTempData():
    global AllData, Input, TempData, ProductsIFR, ProductSetNumber
    TempData["TypeOfDensity"] = TempData["TypeOfDensity"].replace(np.nan , "TBD")
    FoundIndexs = []
    for CurrentRowChecked in range(len(TempData)):
        CurrentRowSelected = TempData.loc[CurrentRowChecked : CurrentRowChecked]
        CurrentProductName = CurrentRowSelected["Product Name"]
        CurrentProductName = ''.join(CurrentProductName.apply(str))
        if CurrentProductName == "":
            continue
        ProductSetNumber = ProductSetNumber + 1
        FoundIndexs = []
        
        CurrentSize = CurrentRowSelected["Size"]
        CurrentForce = CurrentRowSelected["Force"]
        CurrentDensity = CurrentRowSelected["TypeOfDensity"]
        CurrentExtraAttrs = CurrentRowSelected["ExtraAttrs"]
        CurrentSize = ''.join(CurrentSize.apply(str))
        CurrentForce = ''.join(CurrentForce.apply(str))
        CurrentDensity = ''.join(CurrentDensity.apply(str))
        CurrentExtraAttrs = "".join(CurrentExtraAttrs.apply(str))
        
        
        Name = CurrentRowSelected["Product Name"]
        Name = ''.join(Name.apply(str))
        
        Companies = TempData["Company"].where((TempData["Force"] == CurrentForce) & (TempData["TypeOfDensity"] == CurrentDensity) & (TempData["ExtraAttrs"] == CurrentExtraAttrs) & (TempData["Size"] == CurrentSize))
        Prices = TempData["Price"].where((TempData["Force"] == CurrentForce) & (TempData["TypeOfDensity"] == CurrentDensity) & (TempData["ExtraAttrs"] == CurrentExtraAttrs)  & (TempData["Size"] == CurrentSize))
        Hrefs = TempData["Href"].where((TempData["Force"] == CurrentForce) & (TempData["TypeOfDensity"] == CurrentDensity) & (TempData["ExtraAttrs"] == CurrentExtraAttrs)  & (TempData["Size"] == CurrentSize))
        Companies = Companies.dropna()
        Prices = Prices.dropna()
        Hrefs = Hrefs.dropna()
        
        CombinedNamesPrices = pd.DataFrame({"Company Names" : Companies , "Price For Company Name" : Prices , "Hrefs" : Hrefs})
        
        CombinedNamesPrices = CombinedNamesPrices.sort_values(by = ["Price For Company Name"])
        Companies = CombinedNamesPrices["Company Names"]
        Prices = CombinedNamesPrices["Price For Company Name"]
        Hrefs = CombinedNamesPrices["Hrefs"]
        Hrefs = Hrefs.dropna()
         
        Companies = Companies.dropna()
        Prices = Prices.dropna()
        BestPrice = Prices.iloc[0]
        AllTempPrices = pd.Series({})
        for i in range(len(Prices)):
            TempPrice = Prices.iloc[i]
            if TempPrice > 20.00:
                TempPrice = "N/A C1"
            else:
                TempPrice = '{0:.2f}'.format(TempPrice)
            TempAppender = pd.Series([TempPrice])
            AllTempPrices = AllTempPrices._append(TempAppender)
        IncVATPrices = AllTempPrices
        IncVATPrices = "£" + Prices.astype(str).str.cat(sep=' \n£') + " "
        
        BestPrice = round(((BestPrice - (BestPrice*0.20)) - 0.10) , 2)
        BestPrice = '{0:.2f}'.format(BestPrice)
        BestPrice = "£" + str(BestPrice)
        AllTempPrices = pd.Series({})
        for i in range(len(Prices)):
            TempPrice = Prices.iloc[i]
            TempPrice = TempPrice - (TempPrice*0.20)
            if TempPrice > 20.00:
                TempPrice = "N/A C1"
            else:
                TempPrice = '{0:.2f}'.format(TempPrice)
            TempAppender = pd.Series([TempPrice])
            AllTempPrices = AllTempPrices._append(TempAppender)
        ExVATPrices = AllTempPrices
        ExVATPricesSeries = ExVATPrices
    
        SeriesCompanies = Companies
        Companies = Companies.str.cat(sep=' \n') + " "
        ExVATPrices = "£" + ExVATPrices.astype(str).str.cat(sep=' \n£') + " "
        Hrefs = Hrefs.str.cat(sep=' \n') + " "
        
        AllCompanies = ["Travis Perkins" , "Jewson" , "Selco" , "BnQ" , "Wickes" , "BMNW"]
        for CCCompany in AllCompanies:
            if CCCompany not in Companies:
                Companies = Companies + "\n" + CCCompany
                Temp = pd.Series([CCCompany])
                SeriesCompanies = SeriesCompanies._append(Temp)
                if CCCompany == "BMNW":
                    IncVATPrices = IncVATPrices + "\nN/A C2"
                    ExVATPrices = ExVATPrices + "\nN/A C2"
                    ExVATPricesSeries = ExVATPricesSeries._append(pd.Series(["N/A C2"]))
                else:
                    ExVATPrices = ExVATPrices + "\nNot Found"
                    IncVATPrices = IncVATPrices + "\nNot Found"
                    ExVATPricesSeries = ExVATPricesSeries._append(pd.Series(["Not Found"]))
        
        
        FoundCompanies = ""
        FoundPrices = ""
        for i in range(len(ExVATPricesSeries)):
            CurrentCheckedPrice = ExVATPricesSeries.iloc[i]
            CurrentCheckedCompany = SeriesCompanies.iloc[i]
            if CurrentCheckedCompany not in FoundCompanies:
                FoundCompanies = FoundCompanies + CurrentCheckedCompany + "\n"
                if CurrentCheckedPrice != "Not Found" and CurrentCheckedPrice != "N/A" and  CurrentCheckedPrice != "N/A C1" and CurrentCheckedPrice != "N/A C2":
                    FoundPrices = FoundPrices + "£" + CurrentCheckedPrice + "\n"
                else:
                    FoundPrices = FoundPrices + CurrentCheckedPrice + "\n"
        
        FoundIndexs = TempData.index.where((TempData["Force"] == CurrentForce) & (TempData["TypeOfDensity"] == CurrentDensity) & (TempData["ExtraAttrs"] == CurrentExtraAttrs)  & (TempData["Size"] == CurrentSize)).dropna()
        for IndexVal in FoundIndexs:
            TempUsedRow = TempData.loc[IndexVal : IndexVal]
            TempUsedRow["Product Set"] = TempUsedRow["Product Set"].replace(np.nan , Name)
            ProductsIFR = ProductsIFR._append(TempUsedRow)

        for IndexVal in FoundIndexs:
            TempData = TempData.drop(index = IndexVal)
        
        TempCondensedRow = pd.DataFrame({
            "Product Name": Name,
            "Company": Companies,
            "Ex. VAT Prices": ExVATPrices,
            "Inc. VAT Prices" : IncVATPrices,
            "Href": Hrefs,
            "Force": CurrentForce,
            "TypeOfDensity": CurrentDensity,
            "ExtraAttrs" : CurrentExtraAttrs,
            "Product Set" : Name,
            "Size" : CurrentSize,
            "human col" : ProductSetNumber,
            "IMAGE COL" : "INSERT TEMP IMAHGE HERE",
            "Best Price" : BestPrice,
            "Best Companies" : FoundCompanies,
            "Best Prices" : FoundPrices
            }
                                        
                                        , index=[0])
        AllData = AllData._append(TempCondensedRow, ignore_index = True)
    TempData = pd.DataFrame(columns = ["Product Set" , "Product Name" , "Company" , "Ex. VAT Prices" , "Size"]) 

ProductSetNumber = 0    
AbsoluteAllData = pd.DataFrame(columns = ["Product Set" , "Product Name" , "Company" ,  "Price" , "Size"]) #relic
AllData = pd.DataFrame(columns = ["Product Set" , "Product Name" , "Company" , "Ex. VAT Prices", "Inc. VAT Prices" , "Size"]) 
TempData = pd.DataFrame(columns = ["Product Set" , "Product Name" , "Company" , "Ex. VAT Prices" , "Inc. VAT Prices" , "Size"]) 
ProductsIFR = pd.DataFrame(columns = ["Product Set" , "Product Name" , "Company" , "Ex. VAT Prices" , "Inc. VAT Prices" , "Size"]) #relic


Inputs = ["concrete block 100mm" , "concrete block 140mm" , "concrete block 215mm" , "foundation block" , "Concrete Common"]
CurrentSizeInputs = ["100mm" , "140mm" , "215mm" , "Foundation" , "Common"]
for i in range(len(Inputs)):
    Input = Inputs[i].replace(" " , "-").replace("." , "-")
    CurrentSizeInput = CurrentSizeInputs[i]
    url = TravisPerkinsCreateSearch(Input)
    TravisPerkinsGetPricesNamesFromSearch(url)
    url = SelcoCreateSearch(Input)
    SelcoGetPricesNamesFromSearch(url)
    url = JewsonsCreateSearch(Input)
    JewsonGetPriceNamesFromSearch(url)
    url = WickesCreateSearch(Input)
    WickesGetPricesNamesFromSearch(url)
    url = BnQCreateSearch(Input)
    if Input != "concrete block 215mm".replace(" " , "-").replace("." , "-"):
        BnQGetPricesNamesfromSearch(url)
    url = BMNWCreateSearch(Input)
    BMNWGetPricesNamesfromSearch(url)
    TempData["Size"] = TempData["Size"].replace("" , Input)
    CondenseTempData()
    AllData["Size"] = AllData["Size"].replace("" , Input)

os.system("cls")
os.system("cls")
try:
    Comparison = pd.read_csv(OutputDir , encoding="cp1252")
except:
    Comparison = AllData["Ex. VAT Prices"]
    AllData.to_csv(OutputDir , encoding="cp1252")

os.system("cls")
os.system("cls") 
for i in range(len(AllData)):
    try:
        if Comparison["Ex. VAT Prices"].iloc[i] == AllData["Ex. VAT Prices"].iloc[i]:
            pass
        else:
            print("UH OH")
            AllData.to_csv(OutputDir , encoding="cp1252")
    except:
        AllData.to_csv(OutputDir , encoding="cp1252")
        break


