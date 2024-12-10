from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time

service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://facecomparison.toolpie.com/")


file_input_1 = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "validatedCustomFile"))
)

file_input_2 = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "validatedCustomFile2"))
)

submit_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "inputSubmit"))
)


jay = '/Users/emillau/Desktop/Work/python-web-automation/images/jay.png'
yoga = '/Users/emillau/Desktop/Work/python-web-automation/images/yoga.png'

file_input_1.send_keys(jay)  
file_input_2.send_keys(yoga)  
submit_button.click()

time.sleep(4)
result_element = driver.find_element(By.CSS_SELECTOR, ".text-warning.font-weight-bold")
result = result_element.text

print(result)

driver.quit()


