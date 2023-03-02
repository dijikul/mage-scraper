from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import urllib.request
import time

# set the path to the chromedriver executable file
driver_path = "c:/Users/dijikul/Downloads/geckodriver.exe"

# set the URL of the website with the images to download
url = "https://www.mage.space/u/CVn9mYCFxfXnMavykVyE7iIn75N2"

# initialize the Firefox driver
driver = webdriver.Firefox(executable_path=driver_path)

# Wait for Firefox to load
# time.sleep(1)

# navigate to the website
driver.get(url)

# Give ample time for the page to load. Pause here to scroll down until we find a better way to handle
#time.sleep(1)

# find all div elements with the role="gridcell"
grid_cells = driver.find_elements(By.XPATH, "//div[@role='gridcell']")

# iterate over the grid cells
for i, cell in enumerate(grid_cells):
    # click on the cell to open the modal
    cell.click()

    # wait for download link to be ready
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@download]")))

    # find the download link in the modal
    download_link = driver.find_element(By.XPATH, "//a[@download]")

    # get the source URL of the image to download
    img_url = download_link.get_attribute("href")

    # obtain just the filename
    filename = img_url.split('/')[-1]

    # download the image
    print(f"Downloading {i+1}/{len(grid_cells)}: {filename}")
    download_link.click()

    # close the modal
    close_button = driver.find_element(By.CSS_SELECTOR, ".mantine-Modal-close")
    close_button.click()

# close the Firefox driver
driver.quit()