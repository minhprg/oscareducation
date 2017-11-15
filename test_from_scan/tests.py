from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Create your tests here.

from promotions.utils import insertion_sort_file
import qrtools


class FileOrder():
    def __init__(self, n):
        self.name = n


class UploadingCopiesTest(TestCase):

    def test_sorting_copies(self):
        filelist = [
            FileOrder("scan001.jpg"),
            FileOrder("scan002.jpg"),
            FileOrder("scan005.jpg"),
            FileOrder("scan011.jpg"),
            FileOrder("scan003.jpg"),
            FileOrder("scan101.jpg"),
            FileOrder("scan102.jpg"),
            FileOrder("scan301.jpg"),
            FileOrder("scan010.jpg")
        ]
        insertion_sort_file(filelist)
        self.assertTrue(check_order(filelist))


def check_order(filelist):
    for i in range(0, len(filelist)-1):
        if filelist[i].name > filelist[i + 1].name:
            return False
    return True



class AccountTestCase(LiveServerTestCase):

    def setUp(self):

        driver = webdriver.Chrome('/bin/chromedriver')  # Optional argument, if not specified will search path.
        driver.get('http://www.google.com/xhtml');

        self.selenium = driver
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_register(self):
        selenium = self.selenium
        #Opening the link we want to test
        selenium.get('http://127.0.0.1:8000')
        time.sleep(10)

