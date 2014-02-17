from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import contextlib
import time


def delete_post(usr, pwd, post):
    print "STARTING DELETE"
    timeout_counter = 0

    with contextlib.closing(webdriver.PhantomJS()) as driver:
        # or you can use Firefox()
        # or you can use Chrome(executable_path="/usr/bin/chromedriver")
        print "--Opening facebook..."
        driver.get("http://www.facebook.org")
        assert "Facebook" in driver.title

        print "--Logging in..."
        while True:
            try:
                elem = driver.find_element_by_id("email")
                break
            except:
                print "----Waiting"
                time.sleep(1)
                timeout_counter += 1
                if timeout_counter == 5:
                    raise Exception("TimedOut")

        timeout_counter = 0
        elem.send_keys(usr)

        while True:
            try:
                elem = driver.find_element_by_id("pass")
                break
            except:
                print "----Waiting"
                time.sleep(1)
                timeout_counter += 1
                if timeout_counter == 5:
                    raise Exception("TimedOut")

        timeout_counter = 0
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)

        print "--Retrieving post..."
        driver.get(post)

        print "--Expanding arrow options..."
        elem = driver.find_elements_by_xpath("//a[contains(@class,'_5pbj _p')]")
        while len(elem) == 0:
            print '----Waiting'
            print elem
            time.sleep(2)
            timeout_counter += 1
            if timeout_counter == 5:
                raise Exception("TimedOut")
            elem = driver.find_elements_by_xpath(
                "//a[contains(@class,'_5pbj _p')]")

        timeout_counter = 0
        elem[0].click()

        print "--Finding delete option..."
        elem = driver.find_elements_by_xpath("//div[contains(@class,'_54ng')]")
        while len(elem) == 0:
            print '----Waiting'
            print elem
            time.sleep(2)
            timeout_counter += 1
            if timeout_counter == 5:
                raise Exception("TimedOut")
            elem = driver.find_elements_by_xpath(
                "//div[contains(@class,'_54ng')]")

        timeout_counter = 0
        elem = elem[0]
        links = elem.find_elements_by_xpath('.//a')
        while len(links) == 0:
            print '----Waiting'
            print elem
            time.sleep(2)
            timeout_counter += 1
            if timeout_counter == 5:
                raise Exception("TimedOut")
            links = elem.find_elements_by_xpath('.//a')

        print "--Clicking delete..."
        timeout_counter = 0
        links[2].click()

        print "--Finding delete confirmation 'enter'..."
        elem = driver.find_elements_by_css_selector("button._42fu:nth-child(1)")
        while len(elem) == 0:
            print '----Waiting'
            print elem
            time.sleep(2)
            timeout_counter += 1
            if timeout_counter == 5:
                raise Exception("TimedOut")
            elem = driver.find_elements_by_css_selector(
                "button._42fu:nth-child(1)")

        print "--Deleting..."
        elem[0].click()

        print "--Deleted"