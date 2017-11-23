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
    exType = ("algebraicEquation", "algebraicEquation", "algebraicInequation", "algebraicInequation",
              "algebraicExpression", "algebraicExpression","algebraicSystem", "algebraicSystem")
    instruction = ("Eq1", "Eq2", "Ineq1", "Ineq2", "Expr1", "Expr2", "Syst1", "Syst2")
    equations = ("4*x + 10 = 14", "2*x + 2 = 22", "2*x + 2 < 22", "2*x + 2 > 22", "8*2+4", "8*(2+4)", "x=1", "x+y=3")
    secondEquations = ("no", "no", "no", "no", "no", "no", "y=10", "y=1") # only for system of equation

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
        # time.sleep(4)
        element = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/a/img")
        element.click()
        element = driver.find_element_by_partial_link_text("Ajouter un test en ligne")
        element.click()
        element = driver.find_element_by_id("test_name")
        element.click()
        now = datetime.now()
        test_name_time = now.strftime("%y_%m_%d/%H_%M_%S")
        element.send_keys(test_name_time)

        select = Select(driver.find_element_by_xpath("//select[@ng-model='stage17SelectedSkill']"))
        select.select_by_value("TG6-U3-T1")
        element = driver.find_element_by_id("addSkillToTestButtonForStage17")
        element.click()
        # time.sleep(3)

        # element = driver.find_element_by_partial_link_text("er le test")
        element = driver.find_element_by_xpath("//button[@type='submit']")
        element.click()
        time.sleep(2)

        # Change questions
        element = driver.find_element_by_partial_link_text("NOUVEAU")
        element.click()

        element = driver.find_element_by_xpath("//input[@ng-model='question.instructions']")
        element.send_keys(instruction[0])
        select = Select(driver.find_element_by_xpath("//select[@ng-model='question.type']"))
        select.select_by_value(exType[0])
        element = driver.find_element_by_xpath("//input[@ng-model='question.eq1']")
        element.send_keys(equations[0], Keys.ENTER)

        for i in range(1,8):
            element = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/form/div[1]/button")
            element.click()
            elements = driver.find_elements_by_xpath("//input[@ng-model='question.instructions']")
            elements[i].send_keys(instruction[i])
            elements = driver.find_elements_by_xpath("//select[@ng-model='question.type']")
            select = Select(elements[i])
            select.select_by_value(exType[i])
            elements = driver.find_elements_by_xpath("//input[@ng-model='question.eq1']")
            elements[i].send_keys(equations[i], Keys.ENTER)
            if "Syst" in exType[i]:
                elements = driver.find_elements_by_xpath("//input[@ng-model='question.eq2']")
                elements[i-6].send_keys(secondEquations[i], Keys.ENTER)


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
        element.send_keys("x=42")

        element = driver.find_element_by_id("buttonAlgebraic1")
        element.click()

        element = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/form/input[2]")
        element.click()


        # Disconnect Sutdent en reconnect professor
        element = driver.find_element_by_class_name("icon")
        element.click()
        element = driver.find_element_by_partial_link_text("connecter")
        element.click()
        element = driver.find_element_by_id("id_username")
        element.send_keys("selenium_prof", Keys.ENTER)
        element = driver.find_element_by_id("id_password")
        element.send_keys("selenium_prof", Keys.ENTER)

        # Got to the test
        element = driver.find_element_by_partial_link_text("Selenium_class")
        element.click()
        element = driver.find_element_by_partial_link_text("Mes Tests")
        element.click()
        element = driver.find_element_by_partial_link_text(test_name_time)
        element.click()
        element = driver.find_element_by_partial_link_text("Student Selenium")
        element.click()

        # Here we must verify the answer
        time.sleep(5)

        # Delete test
        element = driver.find_element_by_partial_link_text("Test")
        element.click()
        element = driver.find_element_by_partial_link_text("Effacer")
        element.click()
        element = driver.find_element_by_xpath("//button[@type='submit']")
        element.click()
        element = driver.find_element_by_class_name("icon")
        element.click()




    except TimeoutException:
        print("Timeout")


if __name__ == "__main__":
    driver = init_driver()
    lookup(driver)
    time.sleep(5)
    # driver.quit()
