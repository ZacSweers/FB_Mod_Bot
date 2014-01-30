__author__ = 'pandanomic'

import unittest


class TestTagValidity(unittest.TestCase):
    def setUp(self):
        self.test_tags = ["Looking", "Rooming", "Offering"]
        self.junk = """here's somet other text because yeah more text to
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


if __name__ == '__main__':
    unittest.main()