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


input()

quality_selector = "#wrapper > div.mr-tools.mrt-top > div > div > div.float-left > div:nth-child(3) > button"
high_quality_selector = "#wrapper > div.mr-tools.mrt-top > div > div > div.float-left > div.rt-item.show > div > a:nth-child(1)"
while True:
	try:
		nextbutton = driver.find_element(by=By.CSS_SELECTOR, value="#divslide > div.navi-buttons.hoz-controls.hoz-controls-rtl > a.nabu.nabu-left.hoz-next > div")
		canvas = driver.find_element(by=By.CSS_SELECTOR, value="#divslide > div.divslide-wrapper > div.ds-item.active > div > canvas")
		settingsbutton = driver.find_element(by=By.CSS_SELECTOR, value="#header > div > div.auto-div > div.float-right.hr-right > div.hr-setting.mr-2 > a")

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

tottime = 0
ending_url = ""
data = driver.get_screenshot_as_png()

location = canvas.location
csize = canvas.size
w, h = csize['width'], csize['height']
x, y = location["x"], location["y"]

pil_image = Image.open(io.BytesIO(data))
np_array = np.array(pil_image)
blank_px = [255, 255, 255, 0]
x0, y0 = x, y
x1, y1 = x+w, y+h

cropped_box = np_array[y0:y1, x0:x1]

driver.set_window_size(1417, 1530)
driver.execute_script("document.body.style.zoom='200%'")
print("Calibrating...")

image_pixel_x = 0

while True:
	if cropped_box[0, image_pixel_x][0] != 17:
		if cropped_box[0, image_pixel_x][1] != 17:
			if cropped_box[0, image_pixel_x][2] != 17:
				break

	image_pixel_x += 1

margin_len = image_pixel_x

location = canvas.location
csize = canvas.size
w, h = csize['width'], csize['height']
x, y = location["x"], location["y"]

img_list = []

double_page_margin = 30

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
	pil_image.save("test.png")
	np_array = np.array(pil_image)
	blank_px = [255, 255, 255, 0]
	x0, y0 = x, y
	x1, y1 = x+w, y+h

	front_x = margin_len
	back_x = w - margin_len
	cropped_box = np_array[y0:y1, x0:x1]
	cropped_box = cropped_box[0:h, front_x:back_x]
	if cropped_box[0, margin_len + 1][0] == 17:
		if cropped_box[31, margin_len + 1][0] != 17:
			print("Double page!")
			cropped_box = np_array[y0:y1, x0:x1]
			cropped_box = cropped_box[30:h-30, 0:w]
		if cropped_box[0, margin_len + 1][1] == 17:
			if cropped_box[0, margin_len + 1][2] == 17:
				sleep(0.1)
				attempts += 1
				if attempts < 10:
					continue
	attempts = 0
	
	pil_image = Image.fromarray(cropped_box, 'RGBA')
	pil_image = pil_image.convert("RGB")
	img_list.append(pil_image)

	endtime = time.time()
	tottime += endtime
	nextbutton.click()
	pagenum += 1
	sleep(0.05)

img_list[0].save(
				f"downloads/{mangatitle}.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=img_list[1:]
			)
print(f"Volume saved to downloads/{mangatitle}.pdf. Quitting because autocontinue is disabled!")

driver.quit()