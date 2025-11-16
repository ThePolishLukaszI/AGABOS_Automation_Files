from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys
import pandas as pd
import os

""" AS OF 16/11/2025, Pre-loaded edge profiles still need to be update"""

def MainDriverLoad():
    Extra = webdriver.EdgeOptions() 
    #Extra.add_argument("user-data-dir=C:\\Users\\TooBrainCels\\AppData\\Local\\Microsoft\\Edge\\Data1")
    Extra.add_argument("--log-level=3")  # Suppresses unnecessary logs
    return  webdriver.Edge(options=Extra)

def ViewDriverLoad():
    Extra = webdriver.EdgeOptions() 
    #Extra.add_argument("user-data-dir=C:\\Users\\TooBrainCels\\AppData\\Local\\Microsoft\\Edge\\Data2") 
    Extra.add_argument("--log-level=3")  # Suppresses unnecessary logs
    return webdriver.Edge(options=Extra)

def UniversalOptionsLoad():
    pd.set_option('display.max_colwidth', None)
    pd.reset_option('display.max_colwidth', None)
    sys.stderr = open(os.devnull, "w")