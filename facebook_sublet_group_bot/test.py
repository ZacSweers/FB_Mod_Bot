__author__ = 'pandanomic'

import unittest


class TestTagValidity(unittest.TestCase):
    def setUp(self):
        self.test_tags = ["Looking", "Rooming", "Offering"]
        self.junk = """here's some other text because yeah more text to
            to illustrate lots more text here in the rest of the post"""

    def test_regular(self):
        from fb_bot import check_tag_validity
        for tag in self.test_tags:
            self.assertTrue(check_tag_validity("(" + tag + ")"))
            self.assertTrue(check_tag_validity("{" + tag + "}"))
            self.assertTrue(check_tag_validity("[" + tag + "]"))
            self.assertTrue(check_tag_validity("(" + tag + "]"))
            self.assertTrue(check_tag_validity("{" + tag + "]"))
            self.assertTrue(check_tag_validity("(" + tag + "}"))
            self.assertTrue(check_tag_validity("{" + tag + ")"))
            self.assertFalse(check_tag_validity(tag + ")"))
            self.assertFalse(check_tag_validity("{" + tag))
            self.assertFalse(check_tag_validity(tag))

    def test_misc(self):
        from fb_bot import check_tag_validity
        for tag in self.test_tags:
            self.assertTrue(check_tag_validity("(" + tag + ") sometjunk"))
            self.assertFalse(check_tag_validity("{" + tag + "}" + self.junk))
            self.assertFalse(check_tag_validity("dsflkj{" + tag.lower() + ")"))
            self.assertFalse(check_tag_validity("dsflkj {" + tag.lower() + ")"))
            self.assertTrue(check_tag_validity("-(" + tag + ")"))
            self.assertTrue(check_tag_validity("*(" + tag + ")"))
            self.assertTrue(check_tag_validity("* (" + tag + ")"))
            self.assertTrue(check_tag_validity(" (" + tag + ")"))
            self.assertTrue(check_tag_validity("(" + tag + "):"))
            self.assertTrue(check_tag_validity("(" + tag + ") :"))


class TestPriceValidity(unittest.TestCase):
    def setUp(self):
        self.junk = """here's some other text because yeah more text to
            to illustrate lots more text here in the rest of the post"""

    def test_regular_month(self):
        from fb_bot import check_price_validity
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
        from fb_bot import check_price_validity
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
        from fb_bot import check_price_validity
        self.assertTrue(check_price_validity("Blah$ blah" + self.junk))
        self.assertTrue(check_price_validity("Blah300 per month" + self.junk))
        self.assertTrue(check_price_validity("Blah blah 300permonth"))
        self.assertTrue(check_price_validity("Blah blah300/monthblah"))
        self.assertTrue(check_price_validity("Blah blah 300amonth"))

    def test_regular_mon(self):
        from fb_bot import check_price_validity
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
        from fb_bot import check_price_validity
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
        from fb_bot import check_price_validity
        self.assertTrue(check_price_validity("Blah$ blah" + self.junk))
        self.assertTrue(check_price_validity("Blah300 per mon" + self.junk))
        self.assertTrue(check_price_validity("Blah blah 300permon"))
        self.assertTrue(check_price_validity("Blah blah300/monblah"))
        self.assertTrue(check_price_validity("Blah blah 300amon"))

    def test_regular_mo(self):
        from fb_bot import check_price_validity
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
        from fb_bot import check_price_validity
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
        from fb_bot import check_price_validity
        self.assertTrue(check_price_validity("Blah$ blah" + self.junk))
        self.assertTrue(check_price_validity("Blah300 per mo" + self.junk))
        self.assertTrue(check_price_validity("Blah blah 300permo"))
        self.assertTrue(check_price_validity("Blah blah300/moblah"))
        self.assertTrue(check_price_validity("Blah blah 300amo"))


if __name__ == '__main__':
    unittest.main()