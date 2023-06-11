# Import libraries
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

def scrape(RESEARCH, NUMBER_OF_IMAGE, dest_folder,CurNbImages):
    # Set up WebDriver
    PATH = r".\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get(f"https://duckduckgo.com/?q={RESEARCH}&iar=images&iax=images&ia=images")
    
    
    driver.implicitly_wait(5)

    # Create dest_folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Scrape images and save them to the target folder
    for i in range(NUMBER_OF_IMAGE):
        miniature = driver.find_element("xpath", f'//*[@id="zci-images"]/div/div[2]/div/div[{i+2}]')
        miniature.click()
        driver.implicitly_wait(1)
        grandeMiniature = driver.find_element("xpath", "/html/body/div[2]/div[3]/div/div[2]/div/div[1]/div[2]/div/div[1]/div/a/img[1]")
        src = grandeMiniature.get_attribute('src')

        # Open the image in a new window
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(src)

        # Save the image
        image = driver.find_element("xpath", "/html/body/img")
        with open(os.path.join(dest_folder, f'img({i+1+CurNbImages}).png'), 'wb') as file:
            file.write(image.screenshot_as_png)

        # Close the window and switch back to the main window
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    # Clean up
    time.sleep(0.3)
    driver.quit()