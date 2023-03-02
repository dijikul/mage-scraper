from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException

import urllib.request
import time

# set the path to the chromedriver executable file
driver_path = "c:/Users/dijikul/Downloads/geckodriver.exe"

# set the URL of the website with the images to download
url = "https://www.mage.space/u/CVn9mYCFxfXnMavykVyE7iIn75N2"

# initialize the Firefox driver
driver = webdriver.Firefox(executable_path=driver_path)

# Wait for Firefox to load
#time.sleep(1)

# navigate to the website
driver.get(url)

# Give ample time for the page to load. Pause here to scroll down until we find a better way to handle
time.sleep(3)

# initialize image counter
img_count = 0

# Locate the slider thumb element
slider_thumb = driver.find_element(By.CLASS_NAME, "mantine-Slider-thumb")

# Click on the slider thumb element to give focus to it
slider_thumb.click()

# Send the ARROW_LEFT key to move the slider thumb to the left
slider_thumb.send_keys(Keys.HOME)
time.sleep(0.2)

# make the images large for easy scraping

def get_grid_cells():
    # find all div elements with the role="gridcell"
    grid_cells = driver.find_elements(By.XPATH, "//div[@role='gridcell']")
    return grid_cells

grid_cells = get_grid_cells()

# create a list to keep track of the already downloaded elements
downloaded_elements = []


def scan_media(grid_cells):
    for i, cell in enumerate(reversed(grid_cells)):
        global img_count

        # scroll the element into view
        try:
            driver.execute_script("arguments[0].scrollIntoView();", cell)
        except StaleElementReferenceException:
            pass
        
        # wait
        time.sleep(0.5)
        try:
            # click on the cell to open the modal
            cell.click()

        except ElementClickInterceptedException:
            action = ActionChains(driver)
            action.move_to_element(cell).click().perform()

            time.sleep(1)
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

        if filename not in downloaded_elements:
            # download the image
            print(f"Downloading Image Number {img_count + 1}: {filename}")
            download_link.click()
            # add the cell to the downloaded elements list
            downloaded_elements.append(filename)
        else:
            print(f"Already downloaded {filename} - Skipping")


        # close the modal
        time.sleep(0.5)
        close_button = driver.find_element(By.CSS_SELECTOR, ".mantine-Modal-close")
        close_button.click()


        #increment image counter
        img_count += 1

        # wait
        time.sleep(0.5)

        #refresh the grid_cells
        if i+1 == len(grid_cells):
            
            # Go to the end of the page
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # obtain a list of new grid cells
            new_cells = get_grid_cells()
            
            # remove the previous cells we've processed using a list comprehension
            new_cells = [x for x in new_cells if x not in grid_cells ]

            # rescan for more images
            scan_media(grid_cells=new_cells)

scan_media(grid_cells)


# close the Firefox driver
driver.quit()
