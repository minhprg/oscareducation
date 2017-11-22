import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from datetime import datetime


def init_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(15)
    driver.set_page_load_timeout(60)
    return driver


def lookup(driver):
    driver.get("http://127.0.0.1:8000/")

    try:
        element = driver.find_element_by_partial_link_text("connecter")
        element.click()

        driver.switch_to_window(driver.window_handles[1])

        # Connexion professor
        element = driver.find_element_by_id("id_username")
        element.send_keys("selenium_prof", Keys.ENTER)
        element = driver.find_element_by_id("id_password")
        element.send_keys("selenium_prof", Keys.ENTER)

        # Creating the test
        element = driver.find_element_by_partial_link_text("Selenium_class")
        element.click()
        # time.sleep(5)
        element = driver.find_element_by_partial_link_text("Mes Tests")
        element.click()
        time.sleep(4)
        element = driver.find_element_by_partial_link_text("Ajouter un test")
        element.click()
        element = driver.find_element_by_partial_link_text("Ajouter un test en ligne")
        element.click()
        element = driver.find_element_by_id("test_name")
        element.click()
        now = datetime.now()
        test_name_time = now.strftime("%y_%m_%d/%H_%M_%S")
        element.send_keys(test_name_time)
        # time.sleep(2)
        # element = driver.find_element_by_partial_link_text("rieures")
        # element.click()
        select = Select(driver.find_element_by_xpath("//select[@ng-model='stage17SelectedSkill']"))
        select.select_by_value("TG6-U3-T1")
        element = driver.find_element_by_id("addSkillToTestButtonForStage17")
        element.click()
        time.sleep(3)

        # element = driver.find_element_by_partial_link_text("er le test")
        element = driver.find_element_by_xpath("//button[@type='submit']")
        element.click()
        time.sleep(2)

        # Change questions
        element = driver.find_element_by_partial_link_text("NOUVEAU")
        element.click()
        element = driver.find_element_by_xpath("//input[@ng-model='question.instructions']")
        element.send_keys("Eq1")
        select = Select(driver.find_element_by_xpath("//select[@ng-model='question.type']"))
        select.select_by_value("algebraicEquation")

        element = driver.find_element_by_xpath("//input[@ng-model='question.eq1']")
        element.send_keys("4*x + 10 = 14", Keys.ENTER)

        time.sleep(2)
        # element = driver.find_element_by_xpath("//button[@class='btn btn-success']")
        element = driver.find_element_by_xpath("//button[@ng-click='addQuestion()']")
        element.click()

        elements = driver.find_elements_by_xpath("//input[@ng-model='question.instructions']")
        elements[1].send_keys("Eq2")
        elements = driver.find_elements_by_xpath("//select[@ng-model='question.type']")
        select = Select(elements[1])
        select.select_by_value("algebraicEquation")
        elements = driver.find_elements_by_xpath("//input[@ng-model='question.eq1']")
        elements[1].send_keys("2*x + 2 = 22", Keys.ENTER)

        # Submit the test
        element = driver.find_element_by_xpath("//button[@ng-click='proposeToOscar()']")
        element.click()

        element = driver.find_element_by_partial_link_text("capitulatif du test")
        element.click()

        element = driver.find_element_by_xpath("//button[@type='submit']")
        element.click()

        # Publish the test and logout
        element = driver.find_element_by_xpath("//button[@type='submit']")
        element.click()

        alert = driver.switch_to.alert
        alert.accept()

        element = driver.find_element_by_xpath("//button[@type='submit']")
        element.click()

        element = driver.find_element_by_class_name("icon")
        element.click()

        # Connexion student
        element = driver.find_element_by_partial_link_text("connecter")
        element.click()
        element = driver.find_element_by_id("id_username")
        element.send_keys("student.selenium", Keys.ENTER)
        element = driver.find_element_by_id("id_password")
        element.send_keys("student.selenium", Keys.ENTER)

        element = driver.find_element_by_partial_link_text(test_name_time)
        element.click()

        element = driver.find_element_by_xpath("//button[@type='submit']")
        element.click()

        element = driver.find_element_by_id("text0")
        element.send_keys("x=1")

        element = driver.find_element_by_id("buttonAlgebraic0")
        element.click()

        element = driver.find_element_by_id("text1")
        element.send_keys("x=10")

        element = driver.find_element_by_id("buttonAlgebraic1")
        element.click()

        element = driver.find_element_by_xpath("//button[@type='submit']")
        element.click()





    except TimeoutException:
        print("Timeout")


if __name__ == "__main__":
    driver = init_driver()
    lookup(driver)
    time.sleep(5)
    # driver.quit()
