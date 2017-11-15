from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from seleniumrequests import Firefox
import selenium
from selenium import webdriver
import requests
from selenium.webdriver.common.proxy import Proxy, ProxyType

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
driver = Firefox("/usr/lib/firefox")


driver.get("http://127.0.0.1:8000/accounts/usernamelogin/")
username = driver.find_element_by_id("id_username")
username.send_keys("simon")
form = driver.find_element_by_id('login-form')
form.submit()

wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.ID, 'id_password')))


password = driver.find_element_by_id("id_password")
password.send_keys("simon")
form = driver.find_element_by_id('login-form')
form.submit()


driver.get("http://127.0.0.1:8000/algebra/exercice/creation")

#response = driver.request('POST', 'http://127.0.0.1:8000/algebra/exercice/creation', data={"expression":"2X=1","type":"Equation","solution":"x=1/2","level":"1"})

solution = driver.find_element_by_id("solution")
solution.clear()
solution.send_keys("x=1/2")
form = driver.find_element_by_css_selector('.formgroup')
#driver.find_element_by_id("concat").click()
response = form.submit()
time.sleep(2)
assert "La solution est Ok" in driver.page_source


solution = driver.find_element_by_id("solution")
solution.clear()
solution.send_keys("x=1/5")
form = driver.find_element_by_css_selector('.formgroup')
#driver.find_element_by_id("concat").click()
response = form.submit()
time.sleep(2)
assert "422" in driver.page_source

print("Tous les tests ont reussis")
