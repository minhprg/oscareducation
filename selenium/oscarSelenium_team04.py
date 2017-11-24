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


# On se connect en tant que prof et on creer un test
# Pour ce test on donne deux equations inequations et systemes.
# On publie le test et on se connecte en tant qu'etudiant
# L'etudiant selectionne le test et le rempli en donnant la bonne reponse au numero impairs et la mauvaise au numero pairs:
# Il soumet ses reponseetse deconnecte
# Le prof se connect et regarde les resultat du tests pour cet etudiant
# On verifie avec les couleurs que on a bien une sequence vrai/faux/vrai...
# on quitte la page de l'eleve,on supprime le test pour que se soit propre et on se deconnecte.


def init_driver():
    driver = webdriver.Chrome()


    driver.set_window_size(1800, 1100)
    driver.implicitly_wait(15)
    driver.set_page_load_timeout(60)
    return driver


def lookup(driver):
    # Equation type
    exType = ("algebraicEquation", "algebraicExpression", "algebraicEquation", "algebraicInequation", "algebraicInequation",
              "algebraicSystem", "algebraicSystem")
    # Instruction for exercices
    instruction = ("AutoEq", "Expr", "Eq2", "Ineq1", "Ineq2", "Syst1", "Syst2")

    equations = ("no","8*(3+1)", "2*x + 2 = 22", "x + 2 < 10", "2*x > 5", "x=1", "x+y=3")
    secondEquations = ("no", "no", "no", "no", "no", "y=10", "y=1") # only for system of equation

    solutionTentative = ("x=1000","32", "x=42", "x<8", "x<=42", "x=1","x=5")
    secondSolution = ("no", "no" "no", "no", "no", "y=10", "y=1") # only for system of equation

    # True if we expect a good answer, False otherwise
    exact = (False, True,False,True,False,True,False)

    # Lunch oscar
    driver.get("http://127.0.0.1:8000/")

    t = 0 # delay for demo

    try:

        element = driver.find_element_by_partial_link_text("connecter")
        element.click()

        driver.switch_to_window(driver.window_handles[1])

        # Connexion professor
        element = driver.find_element_by_id("id_username")
        element.send_keys("selenium_prof", Keys.ENTER)
        element = driver.find_element_by_id("id_password")
        time.sleep(t)
        element.send_keys("selenium_prof", Keys.ENTER)

        # Creating the test
        element = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[4]/div/a")
        time.sleep(t)
        element.click()
        element = driver.find_element_by_partial_link_text("Mes Tests")
        element.click()
        time.sleep(t)
        element = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/a/img") # add a new test
        element.click()
        time.sleep(t)
        element = driver.find_element_by_partial_link_text("Ajouter un test en ligne")
        element.click()
        time.sleep(t)
        element = driver.find_element_by_id("test_name")
        element.click()

        now = datetime.now()
        test_name_time = now.strftime("%y_%m_%d/%H_%M_%S")
        element.send_keys(test_name_time)

        select = Select(driver.find_element_by_xpath("//select[@ng-model='stage17SelectedSkill']"))
        select.select_by_value("TG6-U3-T1")
        element = driver.find_element_by_id("addSkillToTestButtonForStage17")
        element.click()
        time.sleep(t)

        element = driver.find_element_by_xpath("//button[@type='submit']")
        element.click()

        # Change questions
        time.sleep(t)
        element = driver.find_element_by_partial_link_text("NOUVEAU")
        element.click()

        elements = driver.find_elements_by_xpath("//input[@ng-model='question.instructions']")
        elements[0].send_keys(instruction[0])
        elements = driver.find_elements_by_xpath("//select[@ng-model='question.type']")
        select = Select(elements[0])
        select.select_by_value(exType[0])
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        element = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/form/ul/li/ul/li/div[1]/input")
        element.click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        element = driver.find_element_by_xpath("//*[@id='buttongen0']")
        element.click()

        # element = driver.find_element_by_xpath("//input[@ng-model='question.instructions']")
        # element.send_keys(instruction[0])
        # select = Select(driver.find_element_by_xpath("//select[@ng-model='question.type']"))
        # select.select_by_value(exType[0])
        # element = driver.find_element_by_xpath("//input[@ng-model='question.eq1']")
        # element.send_keys(equations[0], Keys.ENTER)


        for i in range(1,7):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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
                elements[i-5].send_keys(secondEquations[i], Keys.ENTER)
            # print ("Question "+str(i+1)+" ok")

        # Submit the test
        time.sleep(t)
        # element = driver.find_element_by_xpath("//button[@ng-click='proposeToOscar()']")
        # h = driver.execute_script("return document.body.scrollHeight")
        # script = "window.scrollTo(0, " + str(h-500) + ");"

        element = driver.find_element_by_xpath("//*[@id='submit-pull-request']/span")
        element.click()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        element = driver.find_element_by_partial_link_text("capitulatif du test")
        # element = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/a")
        time.sleep(t)
        element.click()

        time.sleep(t)
        element = driver.find_element_by_xpath("//button[@type='submit']")
        element.click()

        # Publish the test and logout
        time.sleep(t)
        element = driver.find_element_by_xpath("//button[@type='submit']")
        element.click()

        time.sleep(t)
        alert = driver.switch_to.alert
        alert.accept()

        time.sleep(t)
        element = driver.find_element_by_xpath("//button[@type='submit']")
        element.click()

        time.sleep(t)
        element = driver.find_element_by_class_name("icon")
        element.click()

        # Connexion student
        element = driver.find_element_by_partial_link_text("connecter")
        element.click()
        time.sleep(t)
        element = driver.find_element_by_id("id_username")
        element.send_keys("student.selenium", Keys.ENTER)
        element = driver.find_element_by_id("id_password")
        element.send_keys("student.selenium", Keys.ENTER)

        time.sleep(t)
        element = driver.find_element_by_partial_link_text(test_name_time)
        element.click()

        time.sleep(t)
        element = driver.find_element_by_xpath("//button[@type='submit']")
        element.click()

        h = driver.execute_script("return document.body.scrollHeight")

        for i in range(0,7):
            button= "buttonAlgebraic"+str(i)
            if "Syst" in exType[i]:
                element = driver.find_element_by_id("textEq1" + str(i))
                element.send_keys(solutionTentative[i])
                element = driver.find_element_by_id("textEq2" + str(i))
                element.send_keys(secondSolution[i])
            else:
                text = "text" + str(i)
                element = driver.find_element_by_id(text)
                element.send_keys(solutionTentative[i])
            element = driver.find_element_by_id(button)
            time.sleep(t)
            element.click()

            script = "window.scrollTo(0, " + str((i*h) / exType.__len__()) + ");"
            driver.execute_script(script)

        time.sleep(t)
        element = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/form/input[2]")
        element.click()


        # Disconnect Sutdent en reconnect professor
        element = driver.find_element_by_class_name("icon")
        element.click()
        element = driver.find_element_by_partial_link_text("connecter")
        element.click()
        time.sleep(t)
        element = driver.find_element_by_id("id_username")
        element.send_keys("selenium_prof", Keys.ENTER)
        element = driver.find_element_by_id("id_password")
        element.send_keys("selenium_prof", Keys.ENTER)

        # Got to the test
        time.sleep(t)
        element = driver.find_element_by_partial_link_text("Selenium_class")
        element.click()
        time.sleep(t)
        element = driver.find_element_by_partial_link_text("Mes Tests")
        element.click()
        time.sleep(t)
        element = driver.find_element_by_partial_link_text(test_name_time)
        element.click()
        time.sleep(t)
        element = driver.find_element_by_partial_link_text("Student Selenium")
        element.click()

        verif = True
        # Here we must verify the answer
        for i in range(0,6):
            if exact[i]:
                color = "rgba(60, 118, 61, 1)" # green
            else:
                color = "rgba(169, 68, 66, 1)" # red

            xpath = "/html/body/div[2]/div[2]/div[4]/table/tbody/tr/td[2]/table/tbody/tr["+str(i+2)+"]/td/div/div[1]"
            element = driver.find_element_by_xpath(xpath)

            actualcolor = str(element.value_of_css_property("color"))
            if actualcolor != color:
                verif = False


        # Delete test
        time.sleep(t)
        element = driver.find_element_by_partial_link_text("Test")
        element.click()
        time.sleep(t)
        element = driver.find_element_by_partial_link_text("Effacer")
        element.click()
        time.sleep(t)
        element = driver.find_element_by_xpath("//button[@type='submit']")
        element.click()
        element = driver.find_element_by_class_name("icon")
        element.click()

        if verif :
            print ("Correct")
        else:
            print ("Error")

        driver.quit()


    except TimeoutException:
        print("Timeout")


if __name__ == "__main__":
    driver = init_driver()
    lookup(driver)
    time.sleep(5)
    # driver.quit()
