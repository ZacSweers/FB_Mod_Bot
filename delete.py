from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import contextlib
import time


def delete_post(usr, pwd, post):
    print "STARTING DELETE"
    sleep_time = 0

    with contextlib.closing(webdriver.PhantomJS()) as driver:
        # or you can use Firefox()
        # or you can use Chrome(executable_path="/usr/bin/chromedriver")
        print "--Opening facebook..."
        driver.get("http://www.facebook.org")
        time.sleep(sleep_time)
        assert "Facebook" in driver.title

        print "--Logging in..."
        elem = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_id("email"))
        time.sleep(sleep_time)
        elem.send_keys(usr)
        time.sleep(sleep_time)
        elem = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_id("pass"))
        time.sleep(sleep_time)
        elem.send_keys(pwd)
        time.sleep(sleep_time)
        elem.send_keys(Keys.RETURN)
        time.sleep(sleep_time)

        print "--Retrieving post..."
        driver.get(post)
        time.sleep(sleep_time)

        print "--Expanding arrow options..."
        elem = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath("//a[contains(@class,'_5pbj _p')]"))
        time.sleep(sleep_time)
        elem.click()
        time.sleep(sleep_time)

        print "--Finding delete option..."
        elem = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath("//div[contains(@class,'_54ng')]"))
        time.sleep(sleep_time)
        links = WebDriverWait(driver, 10).until(lambda driver : elem.find_elements_by_xpath('.//a'))
        time.sleep(sleep_time)

        print "--Clicking delete..."
        links[2].click()
        time.sleep(sleep_time)

        print "--Finding delete confirmation 'enter'..."
        elem = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_css_selector("button._42fu:nth-child(1)"))
        time.sleep(sleep_time)

        print "--Deleting..."
        elem.click()

        print "Deleted"