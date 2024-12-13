from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time

service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://lib.ebookservice.tw/nt/#account/sign-in")

input_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "accountIdText"))
)

accept_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()='我知道了']"))
)
accept_button = driver.find_element(By.XPATH, "//button[text()='我知道了']")
'登入'
accept_button.click()
account_field = driver.find_element(By.ID, "accountIdText")
account_field.send_keys("D101433294")
password_field = driver.find_element(By.ID, "passwordText")
password_field.send_keys("Zs741014")
password_field.send_keys(Keys.RETURN)


time.sleep(100)

driver.quit()


