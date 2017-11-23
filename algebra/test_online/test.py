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
from selenium.webdriver.common.action_chains import ActionChains
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

solution = driver.find_element_by_id("leftSideMath")
driver.execute_script("arguments[0].innerHTML += arguments[1];", solution, "2x");
solution = driver.find_element_by_id("rightSideMath")
driver.execute_script("arguments[0].innerHTML += arguments[1];", solution, "0");
solution = driver.find_element_by_id("solutionMath")
driver.execute_script("arguments[0].innerHTML += arguments[1];", solution, "x=1/5");
form = driver.find_element_by_css_selector('.formgroup')
#driver.find_element_by_id("concat").click()
response = form.submit()
time.sleep(2)
assert "422" in driver.page_source

driver.get("http://127.0.0.1:8000/algebra/student/training_session")
time.sleep(2)

driver.find_element_by_css_selector("#Q_1").click()
time.sleep(1)
driver.find_element_by_css_selector("#Q_2").click()
time.sleep(1)
driver.find_element_by_css_selector("#Q_4").click()
time.sleep(1)
driver.find_element_by_css_selector("#next").click()
time.sleep(1)

password = driver.find_element_by_id("step1")
password.send_keys("x-23x+2=123")
driver.find_element_by_css_selector("#check").click()
time.sleep(1)
assert "alert-danger" in driver.page_source

driver.get("http://127.0.0.1:8000/algebra/")
time.sleep(1)
driver.close()

#response = driver.request('POST', 'http://127.0.0.1:8000/algebra/exercice/creation', data={"expression":"2X=1","type":"Equation","solution":"x=1/2","level":"1"})
'''time.sleep(3)
solution1 = driver.find_element_by_id("leftSideMath")
solution1.click()
time.sleep(1)
solution2 = driver.find_element_by_css_selector("button[data-name='7']").click()
time.sleep(3)
solution3 = driver.find_element_by_css_selector("button[data-name='right']")
time.sleep(3)
solution2 = driver.find_element_by_css_selector("button[data-name='x']").click()
time.sleep(3)
solution4 = driver.find_element_by_css_selector("button[data-name='x']")
time.sleep(3)
driver.execute_script("arguments[0].click()", solution4);

time.sleep(1)
solution4 = driver.find_element_by_id("rightSideMath")
solution4.click()
time.sleep(1)
solution5 = driver.find_element_by_xpath("//button[@data-value='0']")
solution5.click()
time.sleep(1)
solution6 = driver.find_element_by_id("solutionMath")
solution6.click()
time.sleep(1)
solution7 = driver.find_element_by_xpath("//button[@data-value='x']")
solution7.click()
time.sleep(1)
solution8 = driver.find_element_by_xpath("//button[@data-value='=']")
solution8.click()
time.sleep(1)
solution9 = driver.find_element_by_xpath("//button[@data-value='0']")
time.sleep(1)
solution9.click()
time.sleep(1)
form = driver.find_element_by_css_selector('.formgroup')
#driver.find_element_by_id("concat").click()
response = form.submit()
time.sleep(2)
assert "La solution est Ok" in driver.page_source'''


''''solution = driver.find_element_by_id("leftSideMath")
driver.execute_script("arguments[0].innerHTML += arguments[1];", solution, "2x");
solution = driver.find_element_by_id("rightSideMath")
driver.execute_script("arguments[0].innerHTML += arguments[1];", solution, "0");
solution = driver.find_element_by_id("solutionMath")
driver.execute_script("arguments[0].innerHTML += arguments[1];", solution, "x=1/5");
form = driver.find_element_by_css_selector('.formgroup')
#driver.find_element_by_id("concat").click()
response = form.submit()
time.sleep(2)
assert "422" in driver.page_source'''

print("Tous les tests ont reussis")
