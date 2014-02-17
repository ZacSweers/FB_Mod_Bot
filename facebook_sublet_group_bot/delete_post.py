from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import contextlib
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

__author__ = 'Henri Sweers'


# Deletes a post using selenium and phantomJS
def delete_post(usr, pwd, post, *test):
    print "STARTING DELETE"

    testing = False
    if len(test) != 0:
        testing = True

    with contextlib.closing(webdriver.PhantomJS()) as driver:
        # or you can use Firefox()
        # or you can use Chrome(executable_path="/usr/bin/chromedriver")

        wait = WebDriverWait(driver, 15)

        print "--Opening facebook..."
        driver.get("http://www.facebook.com")

        print "--Logging in..."
        elem = wait.until(ec.presence_of_element_located((By.ID, "email")))
        elem.send_keys(usr)
        elem = wait.until(ec.presence_of_element_located((By.ID, "pass")))
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)

        # Wait for login to finish
        time.sleep(3)

        print "--Retrieving post..."
        driver.get(post)

        print "--Expanding arrow options..."
        elem = wait.until(ec.presence_of_element_located(
            (By.XPATH, "//a[contains(@aria-label,'Post options')]")))
        elem.click()

        print "--Waiting for options to load..."
        elem = wait.until(ec.presence_of_element_located(
            (By.XPATH, "//ul[contains(@class,'_54nf')]")))

        print "--Finding delete option"
        links = elem.find_elements_by_xpath(".//a")

        print "--Clicking delete..."
        if testing:
            links[3].click()
        else:
            links[2].click()

        print "--Finding delete confirmation 'enter'..."
        elem = wait.until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, "button._42fu:nth-child(1)")))

        print "--Deleting..."
        elem.click()

        print "--Deletion complete"