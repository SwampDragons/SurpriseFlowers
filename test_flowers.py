# This is the tests for the flower program!!
import datetime
import json
import os
import unittest

import flowers


class FlowerFileTest(unittest.TestCase):

    def test_load_or_create_flowermap_present(self):
        expected = {"flowerday": 20, "current_month": 6, "email_sent": True}
        with open(flowers.FLOWERDATE_FILE, 'w') as f:
            f.write(json.dumps(expected))
        flowermap = flowers.load_or_create_flowermap()
        self.assertEquals(flowermap, expected)
        os.remove(flowers.FLOWERDATE_FILE)

    def test_load_or_create_flowermap_absent(self):
        if os.path.isfile(flowers.FLOWERDATE_FILE):
            os.remove(flowers.FLOWERDATE_FILE)

        expected = {'flowerday': None, 'current_month': None, 'email_sent': False}
        flowermap = flowers.load_or_create_flowermap()
        self.assertEquals(flowermap, expected)

        with open(flowers.FLOWERDATE_FILE, 'r') as f:
            flowermap = json.loads(f.read())
        self.assertEquals(flowermap, expected)


class EmailerTest(unittest.TestCase):
    def assert_check_emailer(self, todays_date, flowermap, expected):
        email_status = flowers.check_date_for_emailer(flowermap, todays_date)
        self.assertEquals(email_status, expected)

    def test_check_emailer1(self):
        todays_date = datetime.date(2013, 6, 24)
        flowermap = {"flowerday": 23, "current_month": 6, "email_sent": True}
        self.assert_check_emailer(todays_date, flowermap, False)

    def test_check_emailer2(self):
        todays_date = datetime.date(2013, 6, 13)
        flowermap = {"flowerday": 23, "current_month": 6, "email_sent": False}
        self.assert_check_emailer(todays_date, flowermap, False)

    def test_check_emailer3(self):
        todays_date = datetime.date(2013, 6, 13)
        flowermap = {"flowerday": 23, "current_month": 6, "email_sent": False}
        self.assert_check_emailer(todays_date, flowermap, False)

    def test_check_emailer4(self):
        todays_date = datetime.date(2013, 6, 23)
        flowermap = {"flowerday": 23, "current_month": 6, "email_sent": False}
        self.assert_check_emailer(todays_date, flowermap, True)

    def test_check_emailer5(self):
        todays_date = datetime.date(2013, 5, 23)
        flowermap = {"flowerday": 23, "current_month": 6, "email_sent": True}
        self.assert_check_emailer(todays_date, flowermap, False)

    def test_check_emailer6(self):
        todays_date = datetime.date(2013, 5, 23)
        flowermap = {"flowerday": 23, "current_month": 6, "email_sent": False}
        self.assert_check_emailer(todays_date, flowermap, False)


class DateGeneratorTest(unittest.TestCase):
    def assert_date(self, flowermap, expected, todays_date):
        generated_flowermap = flowers.generate_date(flowermap, todays_date)[1]
        self.assertEquals(generated_flowermap, expected)

    def test_check_generator1(self):
        todays_date = datetime.date(2013, 6, 23)
        flowermap = {"flowerday": 23, "current_month": 6, "email_sent": False}
        self.assert_date(flowermap, False, todays_date)

    def test_check_generator2(self):
        todays_date = datetime.date(2013, 6, 23)
        flowermap = {"flowerday": 24, "current_month": 6, "email_sent": True}
        self.assert_date(flowermap, False, todays_date)

    def test_check_generator3(self):
        todays_date = datetime.date(2013, 6, 23)
        flowermap = {"flowerday": 23, "current_month": 5, "email_sent": False}
        self.assert_date(flowermap, True, todays_date)

if __name__ == '__main__':
    unittest.main()
