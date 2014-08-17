import os
import pickle
import sys
import subprocess

__author__ = 'Henri Sweers'

import unittest


# Nifty method for sending notifications on my mac when it's done
def notify_mac():
    if sys.platform == "darwin":
        try:
            subprocess.call(
                ["terminal-notifier", "-message", "Tests done", "-title",
                 "FB_Bot", "-sound", "default"])
        except OSError:
            print "If you have terminal-notifier, this would be a notification"


class TestTagValidity(unittest.TestCase):

    def setUp(self):
        self.test_tags = ["Looking", "Rooming", "Offering", "Parking"]
        self.bad_tags = ["blah", "test", "sublease"]
        self.junk = """here's some other text because yeah more text to
            to illustrate lots more text here in the rest of the post"""

    def test_regular(self):
        from check_and_delete import get_tags
        for tag in self.test_tags:
            self.assertTrue(get_tags("(" + tag + ")"))
            self.assertTrue(get_tags("{" + tag + "}"))
            self.assertTrue(get_tags("[" + tag + "]"))
            self.assertTrue(get_tags("(" + tag + "]"))
            self.assertTrue(get_tags("{" + tag + "]"))
            self.assertTrue(get_tags("(" + tag + "}"))
            self.assertTrue(get_tags("{" + tag + ")"))
            self.assertFalse(get_tags(tag + ")"))
            self.assertFalse(get_tags("{" + tag))
            self.assertFalse(get_tags(tag))

    def test_bad(self):
        from check_and_delete import get_tags
        for tag in self.bad_tags:
            self.assertFalse(get_tags("(" + tag + ")"))
            self.assertFalse(get_tags("{" + tag + "}"))
            self.assertFalse(get_tags("{" + tag + "}{looking}"))
            self.assertFalse(get_tags("[" + tag + "]"))
            self.assertFalse(get_tags("(" + tag + "]"))
            self.assertFalse(get_tags("{" + tag + "]"))
            self.assertFalse(get_tags("(" + tag + "}"))
            self.assertFalse(get_tags("{" + tag + ")"))
            self.assertFalse(get_tags(tag + ")"))
            self.assertFalse(get_tags("{" + tag))
            self.assertFalse(get_tags(tag))

    def test_misc(self):
        from check_and_delete import get_tags
        for tag in self.test_tags:
            self.assertTrue(get_tags("(" + tag + ") sometjunk"))
            self.assertFalse(get_tags("{" + tag + "}" + self.junk))
            self.assertFalse(get_tags("dsflkj{" + tag.lower() + ")"))
            self.assertFalse(get_tags("dsflkj {" + tag.lower() + ")"))
            self.assertTrue(get_tags("-(" + tag + ")"))
            self.assertTrue(get_tags("*(" + tag + ")"))
            self.assertTrue(get_tags("* (" + tag + ")"))
            self.assertTrue(get_tags(" (" + tag + ")"))
            self.assertTrue(get_tags("(" + tag + "):"))
            self.assertTrue(get_tags("(" + tag + ") :"))
            self.assertTrue(get_tags("(" + tag + ")(" + tag + ")"))

    def test_parking(self):
        from check_and_delete import check_for_parking_tag
        tag = "parking"
        self.assertTrue(check_for_parking_tag("(" + tag + ")"))
        self.assertTrue(check_for_parking_tag("{" + tag + "}"))
        self.assertTrue(check_for_parking_tag("[" + tag + "]"))
        self.assertTrue(check_for_parking_tag("(" + tag + "]"))
        self.assertTrue(check_for_parking_tag("{" + tag + "]"))
        self.assertTrue(check_for_parking_tag("(" + tag + "}"))
        self.assertTrue(check_for_parking_tag("{" + tag + ")"))
        self.assertFalse(check_for_parking_tag(tag + ")"))
        self.assertFalse(check_for_parking_tag("{" + tag))
        self.assertFalse(check_for_parking_tag(tag))
        self.assertTrue(check_for_parking_tag("(" + tag + ") sometjunk"))
        self.assertFalse(check_for_parking_tag("{" + tag + "}" + self.junk))
        self.assertFalse(check_for_parking_tag("dsflkj{" + tag.lower() + ")"))
        self.assertFalse(check_for_parking_tag("dsflkj {" + tag.lower() + ")"))
        self.assertTrue(check_for_parking_tag("-(" + tag + ")"))
        self.assertTrue(check_for_parking_tag("*(" + tag + ")"))
        self.assertTrue(check_for_parking_tag("* (" + tag + ")"))
        self.assertTrue(check_for_parking_tag(" (" + tag + ")"))
        self.assertTrue(check_for_parking_tag("(" + tag + "):"))
        self.assertTrue(check_for_parking_tag("(" + tag + ") :"))


class TestPriceValidity(unittest.TestCase):
    def setUp(self):
        self.junk = """here's some other text because yeah more text to
            to illustrate lots more text here in the rest of the post"""

    def test_regular_month(self):
        from check_and_delete import check_price_validity
        self.assertTrue(check_price_validity("Blah blah $ blah"))
        self.assertTrue(check_price_validity("Blah blah 300 per month"))
        self.assertTrue(check_price_validity("Blah blah 300/month"))
        self.assertTrue(check_price_validity("Blah blah 300 / month"))
        self.assertTrue(check_price_validity("Blah blah 300 /month"))
        self.assertTrue(check_price_validity("Blah blah 300/ month"))
        self.assertTrue(check_price_validity("Blah blah 300 per/month"))
        self.assertTrue(check_price_validity("Blah blah 300 a month"))
        self.assertTrue(check_price_validity("Blah blah 300 a/month"))

    def test_embedded_month(self):
        from check_and_delete import check_price_validity
        self.assertTrue(check_price_validity("Blah $ blah" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 per month" + self.junk))
        self.assertTrue(check_price_validity("Blah 300/month" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 / month" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 /month" + self.junk))
        self.assertTrue(check_price_validity("Blah 300/ month" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 per/month" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 a month" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 a/month" + self.junk))

    def test_misc_month(self):
        from check_and_delete import check_price_validity
        self.assertTrue(check_price_validity("Blah$ blah" + self.junk))
        self.assertTrue(check_price_validity("Blah300 per month" + self.junk))
        self.assertTrue(check_price_validity("Blah blah 300permonth"))
        self.assertTrue(check_price_validity("Blah blah300/monthblah"))
        self.assertTrue(check_price_validity("Blah blah 300amonth"))

    def test_regular_mon(self):
        from check_and_delete import check_price_validity
        self.assertTrue(check_price_validity("Blah blah $ blah"))
        self.assertTrue(check_price_validity("Blah blah 300 per mon"))
        self.assertTrue(check_price_validity("Blah blah 300/mon"))
        self.assertTrue(check_price_validity("Blah blah 300 / mon"))
        self.assertTrue(check_price_validity("Blah blah 300 /mon"))
        self.assertTrue(check_price_validity("Blah blah 300/ mon"))
        self.assertTrue(check_price_validity("Blah blah 300 per/mon"))
        self.assertTrue(check_price_validity("Blah blah 300 a mon"))
        self.assertTrue(check_price_validity("Blah blah 300 a/mon"))

    def test_embedded_mon(self):
        from check_and_delete import check_price_validity
        self.assertTrue(check_price_validity("Blah $ blah" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 per mon" + self.junk))
        self.assertTrue(check_price_validity("Blah 300/mon" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 / mon" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 /mon" + self.junk))
        self.assertTrue(check_price_validity("Blah 300/ mon" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 per/mon" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 a mon" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 a/mon" + self.junk))

    def test_misc_mon(self):
        from check_and_delete import check_price_validity
        self.assertTrue(check_price_validity("Blah$ blah" + self.junk))
        self.assertTrue(check_price_validity("Blah300 per mon" + self.junk))
        self.assertTrue(check_price_validity("Blah blah 300permon"))
        self.assertTrue(check_price_validity("Blah blah300/monblah"))
        self.assertTrue(check_price_validity("Blah blah 300amon"))

    def test_regular_mo(self):
        from check_and_delete import check_price_validity
        self.assertTrue(check_price_validity("Blah blah $ blah"))
        self.assertTrue(check_price_validity("Blah blah 300 per mo"))
        self.assertTrue(check_price_validity("Blah blah 300/mo"))
        self.assertTrue(check_price_validity("Blah blah 300 / mo"))
        self.assertTrue(check_price_validity("Blah blah 300 /mo"))
        self.assertTrue(check_price_validity("Blah blah 300/ mo"))
        self.assertTrue(check_price_validity("Blah blah 300 per/mo"))
        self.assertTrue(check_price_validity("Blah blah 300 a mo"))
        self.assertTrue(check_price_validity("Blah blah 300 a/mo"))

    def test_embedded_mo(self):
        from check_and_delete import check_price_validity
        self.assertTrue(check_price_validity("Blah $ blah" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 per mo" + self.junk))
        self.assertTrue(check_price_validity("Blah 300/mo" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 / mo" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 /mo" + self.junk))
        self.assertTrue(check_price_validity("Blah 300/ mo" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 per/mo" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 a mo" + self.junk))
        self.assertTrue(check_price_validity("Blah 300 a/mo" + self.junk))

    def test_misc_mo(self):
        from check_and_delete import check_price_validity
        self.assertTrue(check_price_validity("Blah$ blah" + self.junk))
        self.assertTrue(check_price_validity("Blah300 per mo" + self.junk))
        self.assertTrue(check_price_validity("Blah blah 300permo"))
        self.assertTrue(check_price_validity("Blah blah300/moblah"))
        self.assertTrue(check_price_validity("Blah blah 300amo"))


class TestDeletion(unittest.TestCase):

    def test_regular(self):
        import delete_test

        # Suppress stdout printing
        _stdout = sys.stdout
        null = open(os.devnull, 'wb')
        sys.stdout = null

        # Run test
        self.assertTrue(delete_test.test())

        # Restore stdout printing
        sys.stdout = _stdout


def main():
    print ""
    print "-----------------"
    print "| Running tests |"
    print "-----------------"
    unittest.main()
    notify_mac()


if __name__ == '__main__':
    main()