import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


def init_driver():
    driver = webdriver.Firefox()
    driver.implicitly_wait(15)
    driver.set_page_load_timeout(60)
    return driver


def lookup(driver):
    driver.get("http://127.0.0.1:8000/")
    try:
        element = driver.find_element_by_partial_link_text("connecter")
        element.click()

        driver.switch_to_window(driver.window_handles[1])

        #Connexion
        element = driver.find_element_by_id("id_username")
        element.send_keys("selenium_prof", Keys.ENTER)
        element = driver.find_element_by_id("id_password")
        element.send_keys("selenium_prof", Keys.ENTER)

        #Creating the test
        element = driver.find_element_by_partial_link_text("Selenium")
        element.click()
        element.click()
        time.sleep(5)
        element = driver.find_element_by_partial_link_text("Mes Tests")
        element.click()
        time.sleep(4)
        #element = driver.find_element_by_class_name("pull-right")
        element = driver.find_element_by_xpath("//a[@href='/professor/lesson/4/test/add/']")
        element.click()
        element = driver.find_element_by_partial_link_text("Ajouter un test en ligne")
        element.click()
        time.sleep(5)
        element = driver.find_element_by_id("test_name")
        element.click()
        element.send_keys("Exemple")
        time.sleep(2)
        select = Select(driver.find_element_by_xpath("//select[@ng-model='stage17SelectedSkill']"))
        select.select_by_value("TG6-U4-A1")
        element = driver.find_element_by_id("addSkillToTestButtonForStage17")
        element.click()
        time.sleep(6)

        element = driver.find_element_by_xpath("//button[@type='submit']")
        element.click()
        time.sleep(2)

        element = driver.find_element_by_partial_link_text("modifier")
        element.click()
        element = driver.find_element_by_xpath("//input[@ng-model='question.instructions']")
        element.send_keys("RESOUS")
        select = Select(driver.find_element_by_xpath("//select[@ng-model='question.type']"))
        select.select_by_value("algebraicEquation")

        element = driver.find_element_by_xpath("//input[@ng-model='question.eq1']")
        element.send_keys("4*x + 10 = 14", Keys.ENTER)
        time.sleep(5)
        element = driver.find_element_by_id("submit-pull-request")
        element.click()


        #Deleting the existing question and add

        print("Fini!")

    except TimeoutException:
        print("Box or Button not found in google.com")



if __name__ == "__main__":
    driver = init_driver()
    lookup(driver)
    time.sleep(5)
    #driver.quit()