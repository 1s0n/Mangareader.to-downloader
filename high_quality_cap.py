print("Mangareader downloader, please have at least 200mb of space free on your computer to continue!")

import base64
import json
import os
from time import sleep
import chromedriver_autoinstaller
import os
import fitz  # pip install --upgrade pip; pip install --upgrade pymupdf
from tqdm import tqdm # pip install tqdm


print("Verifying/updating chromedriver...")
driverpath = chromedriver_autoinstaller.install()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")


mangareader_link = input("Link to manga (The link to the first page of the manga): ")
#autocontinue = True if input("Autocontinue (T/F): ").lower() != "f" else False
autocontinue = False
autoc = input("Autocontinue (T/F): ").lower()
if autoc == "t" or autoc == "true":
	autocontinue = True
	ending_url = input("URL to stop downloading: ")
	print("Auto continue enabled!")
else:
	print("Auto continue disabled!")
sleep(2)

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driverpath)

print(driver.get_window_size())


driver.get(mangareader_link)


mangatitle = driver.title
mangatitle = mangatitle.replace("Read ", "")
mangatitle = mangatitle.replace(" in English Online Free", "")

print("Searching for horizontal button")

while True:
	try:
		horizontal_button = driver.find_element(by=By.CSS_SELECTOR, value="#first-read > div.read-tips > div > div.rtl-rows > a:nth-child(2)")
		horizontal_button.click()
		break
	except Exception as e:
		print(e)
		sleep(0.5)

print("Done")
# input()
quality_selector = "#wrapper > div.mr-tools.mrt-top > div > div > div.float-left > div:nth-child(3) > button"
high_quality_selector = "#wrapper > div.mr-tools.mrt-top > div > div > div.float-left > div.rt-item.show > div > a:nth-child(1)"
while True:
	try:
		nextbutton = driver.find_element(by=By.CSS_SELECTOR, value="#divslide > div.navi-buttons.hoz-controls.hoz-controls-rtl > a.nabu.nabu-left.hoz-next > div")
		canvas = driver.find_element(by=By.CSS_SELECTOR, value="#divslide > div.divslide-wrapper > div.ds-item.active > div > canvas")
		settingsbutton = driver.find_element(by=By.CSS_SELECTOR, value="#header > div > div.auto-div > div.float-right.hr-right > div.hr-setting.mr-2 > a")
		break
	except Exception as e:
		sleep(0.5)

if not os.path.isdir("downloads"):
	os.mkdir("downloads")

if not os.path.isdir(f"downloads/{mangatitle}"):
	os.mkdir(f"downloads/{mangatitle}")

pathrn = f"downloads/{mangatitle}"

import time

pagenum = 1

lasturl = driver.current_url

attempts = 0

print("Selecting high quality...")
settingsbutton.click()
qualitybutton = driver.find_element(by=By.CSS_SELECTOR, value=quality_selector)
qualitybutton.click()
high_quality_button = driver.find_element(by=By.CSS_SELECTOR, value=high_quality_selector)
high_quality_button.click()
total_page_num = driver.find_element(by=By.CSS_SELECTOR, value="#divslide > div.navi-buttons.hoz-controls.hoz-controls-rtl > div.nabu-page > span > span.hoz-total-image").text
print("Done")

print(f"Total page num {total_page_num}")

total_page_num = int(total_page_num)

imglist = []

while True:
	if lasturl != driver.current_url:
		break

	print(f"Took screenshot of page {pagenum}")
	starttime = time.time()

	a = driver.print_page()

	doc = fitz.Document(stream=base64.b64decode(a))

	page = list(tqdm(range(len(doc)), desc="pages", leave=False))[0]
	images = tqdm(doc.get_page_images(page), desc="page_images", leave=False)
	if len(images) < 2 and pagenum != total_page_num:
		print("No images found, retrying after 0.5 seconds...")
		sleep(0.5)
		continue
	elif len(images) < 2 and pagenum == total_page_num:
		print("Finished, packing into pdf and exiting...")
		break
	img = list(images)[1]
	xref = img[0]
	image = doc.extract_image(xref)
	pix = fitz.Pixmap(doc, xref)
	pix.save(f"temppng\{pagenum}.png")
	imglist.append(f"temppng/{pagenum}.png")
	try:
		nextbutton.click()
	except selenium.common.exceptions.StaleElementReferenceException:
		print("Stale element reference exception, retrying...")
		nextbutton = driver.find_element(by=By.CSS_SELECTOR, value="#divslide > div.navi-buttons.hoz-controls.hoz-controls-rtl > a.nabu.nabu-left.hoz-next > div")
		nextbutton.click()
		
	pagenum += 1
	sleep(0.1)

print(images)
driver.quit()