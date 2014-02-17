from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import contextlib
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def delete_post(usr, pwd, post):
    print "STARTING DELETE"

    with contextlib.closing(webdriver.Firefox()) as driver:
        # or you can use Firefox()
        # or you can use Chrome(executable_path="/usr/bin/chromedriver")
        print "--Opening facebook..."
        driver.get("http://www.facebook.com")
        assert "Facebook" in driver.title

        print "--Logging in..."
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email")))
        elem.send_keys(usr)
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pass")))
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)

        print "--Retrieving post..."
        driver.get(post)

        print "--Expanding arrow options..."
        elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@class,'_5pbj _p')]")))
        elem.click()

        print "--Finding delete option..."
        elem = driver.find_element_by_xpath("//div[contains(@class,'_54ng')]")
        links = elem.find_elements_by_xpath(".//a")

        print "--Clicking delete..."
        links[2].click()

        print "--Finding delete confirmation 'enter'..."
        elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button._42fu:nth-child(1)")))

        print "--Deleting..."
        elem.click()

        print "--Deleted"