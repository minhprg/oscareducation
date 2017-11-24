## Installation instructions for selenium

###### Install selenium in ve :

```bash
$ sudo pip install selenium
```

###### Install webdrivers

Chrome  :
``` bash
$ wget https://chromedriver.storage.googleapis.com/2.33/chromedriver_linux64.zip
$ unzip chromedriver_linux64.zip
$ sudo cp chromedriver /usr/bin/chromedriver
$ rm chromedriver*
```

Firefox :
``` bash
$ wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
$ tar -xvf geckodriver-v0.19.1-linux64.tar.gz
$ sudo cp geckodriver /usr/bin/geckodriver
$ rm geckodriver*
```


###### Other distributions :

* [Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)
* [Firefox](https://github.com/mozilla/geckodriver/releases)

###### Test code :

``` python
#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()

```

### How run oscarSelenium.py

Create a professor with :
* username : ``selenium_prof``
* password : ``selenium_prof``

Create a class : ``Selenium_class`` and select : ``6e année`` and ``enseignement de transition mathématiques générales`` 

Create a student : 
* Firstname : ``Student``
* Name : ``Selenium``

Generate password for this sudent. 

ID __**must**__ be ``student.selenium``

Set password : ``student.selenium``