import base64
import time
from selenium import webdriver
import os
import chromedriver_autoinstaller
datapath = chromedriver_autoinstaller.install()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(datapath, options=chrome_options)
driver.get("https://google.com")
time.sleep(2)
print("A")
a = driver.print_page()
with open("test.pdf", "wb") as f:
    f.write(base64.b64decode(a))