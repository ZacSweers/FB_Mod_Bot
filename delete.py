from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import contextlib
import time


def delete_post(usr, pwd, post_id):
    print "STARTING DELETE"
    post_to_delete = "http://www.facebook.com/" + post_id
    sleep_time = 3

    with contextlib.closing(webdriver.PhantomJS()) as driver:
        # or you can use Firefox()
        # or you can use Chrome(executable_path="/usr/bin/chromedriver")
        print "Opening facebook..."
        driver.get("http://www.facebook.org")
        time.sleep(sleep_time)
        assert "Facebook" in driver.title

        print "Logging in..."
        elem = driver.find_element_by_id("email")
        time.sleep(sleep_time)
        elem.send_keys(usr)
        time.sleep(sleep_time)
        elem = driver.find_element_by_id("pass")
        time.sleep(sleep_time)
        elem.send_keys(pwd)
        time.sleep(sleep_time)
        elem.send_keys(Keys.RETURN)
        time.sleep(sleep_time)

        print "Retrieving post..."
        driver.get(post_to_delete)
        time.sleep(sleep_time)
        print driver.title

        print "Expanding arrow options..."
        elem = driver.find_element_by_xpath("//a[contains(@class,'_5pbj _p')]")
        time.sleep(sleep_time)
        elem.click()
        time.sleep(sleep_time)

        print "Finding delete option..."
        elem = driver.find_element_by_xpath("//div[contains(@class,'_54ng')]")
        time.sleep(sleep_time)
        links = elem.find_elements_by_xpath('.//a')
        time.sleep(sleep_time)
        print [x.text for x in links]

        print "Clicking delete..."
        links[2].click()
        time.sleep(sleep_time)

        print "Finding delete confirmation 'enter'..."
        elem = driver.find_element_by_css_selector("button._42fu:nth-child(1)")
        time.sleep(sleep_time)

        print "Deleting..."
        elem.click()

        print "Deleted"