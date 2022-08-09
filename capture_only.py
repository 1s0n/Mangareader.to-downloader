print("Mangareader downloader, please have at least 200mb of space free on your computer to continue!")

import os
from time import sleep
import chromedriver_autoinstaller


print("Verifying/updating chromedriver...")
driverpath = chromedriver_autoinstaller.install()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

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

driver = webdriver.Chrome(driverpath)

print(driver.get_window_size())


driver.get(mangareader_link)


mangatitle = driver.title
mangatitle = mangatitle.replace("Read ", "")
mangatitle = mangatitle.replace(" in English Online Free", "")


while True:
	try:
		horizontal_button = driver.find_element(by=By.CSS_SELECTOR, value="#first-read > div.read-tips > div > div.rtl-rows > a:nth-child(2)")
		horizontal_button.click()
		break
	except:
		sleep(0.5)

# input()

while True:
	try:
		nextbutton = driver.find_element(by=By.CSS_SELECTOR, value="#divslide > div.navi-buttons.hoz-controls.hoz-controls-rtl > a.nabu.nabu-left.hoz-next > div")
		canvas = driver.find_element(by=By.CSS_SELECTOR, value="#divslide > div.divslide-wrapper > div.ds-item.active > div > canvas")
		break
	except:
		sleep(0.5)

if not os.path.isdir("downloads"):
	os.mkdir("downloads")

if not os.path.isdir(f"downloads/{mangatitle}"):
	os.mkdir(f"downloads/{mangatitle}")

pathrn = f"downloads/{mangatitle}"

import time

pagenum = 1

lasturl = driver.current_url

from PIL import Image
import numpy as np
import io


driver.set_window_size(1417, 1530)
driver.execute_script("document.body.style.zoom='200%'")
print("Calibrating...")


attempts = 0

while pagenum < 20:
	if lasturl != driver.current_url:
		print("New volume!")
		if not autocontinue:
			img_list[0].save(
				f"downloads/{mangatitle}.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=img_list[1:]
			)
			print(f"Volume saved to downloads/{mangatitle}.pdf. Quitting because autocontinue is disabled!")
			break
		if ending_url == driver.current_url:
			img_list[0].save(
				f"downloads/{mangatitle}.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=img_list[1:]
			)
			print(f"Volume saved to downloads/{mangatitle}.pdf. Quitting because autocontinue is disabled!")
			break
		mangatitle = driver.title
		mangatitle = mangatitle.replace("Read ", "")
		mangatitle = mangatitle.replace(" in English Online Free", "")

		img_list.clear()

	print(f"Took screenshot of page {pagenum}")
	starttime = time.time()

	data = driver.get_screenshot_as_png()


	pil_image = Image.open(io.BytesIO(data))
	pil_image.save(f"downloads/{mangatitle}{pagenum}.png")


	nextbutton.click()
	pagenum += 1
	sleep(0.05)

driver.quit()