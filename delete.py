from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import contextlib
import time


def delete_post(usr, pwd, post_id):
    print "STARTING DELETE"
    post_to_delete = "http://www.facebook.com/" + post_id

    with contextlib.closing(webdriver.PhantomJS()) as driver:
        # or you can use Firefox()
        # or you can use Chrome(executable_path="/usr/bin/chromedriver")
        print "Opening facebook..."
        driver.get("http://www.facebook.org")
        time.sleep(2)
        assert "Facebook" in driver.title

        print "Logging in..."
        elem = driver.find_element_by_id("email")
        elem.send_keys(usr)
        elem = driver.find_element_by_id("pass")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)

        print "Retrieving post..."
        driver.get(post_to_delete)
        time.sleep(2)

        print "Expanding arrow options..."
        elem = driver.find_element_by_xpath("//a[contains(@class,'_5pbj _p')]")
        elem.click()
        time.sleep(2)

        print "Finding delete option..."
        elem = driver.find_element_by_xpath("//div[contains(@class,'_54ng')]")
        links = elem.find_elements_by_xpath('.//a')

        print "Clicking delete..."
        links[2].click()
        time.sleep(2)

        print "Finding delete confirmation 'enter'..."
        elem = driver.find_element_by_css_selector("button._42fu:nth-child(1)")

        print "Deleting..."
        elem.click()

        print "Deleted"