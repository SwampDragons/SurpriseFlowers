# This is the tests for the flower program!!
import datetime
import json
import os
import unittest

import flowers

class FlowerTest(unittest.TestCase):
    def test_date_checker(self):
        self.assertTrue(True)

    def test_check_file_present(self):
        expected = {"flowerday": 20, "current_month": 6, "email_sent": True}
        with open(flowers.filename, 'w') as f:
            f.write(json.dumps(expected))
        flowermap = flowers.check_file(flowers.filename)
        self.assertEquals(flowermap,expected)
        os.remove(flowers.filename)

    def test_check_file_absent(self):        
        if os.path.isfile(flowers.filename):
            os.remove(flowers.filename)

        expected = {'flowerday':None, 'current_month':None, 'email_sent':False}
        flowermap = flowers.check_file(flowers.filename)
        self.assertEquals(flowermap, expected)
        
        with open(flowers.filename, 'r') as f:
            flowermap = json.loads(f.read())
        self.assertEquals(flowermap, expected)

    def test_check_emailer1(self):
        todays_date = datetime.date(2013,6,24)
        flowermap = {"flowerday": 23, "current_month": 6, "email_sent": True}
        expected = 'email not sent'
        self.assert_check_emailer(todays_date, flowermap, expected)

    def test_check_emailer2(self):
        todays_date = datetime.date(2013,6,13)
        flowermap = {"flowerday": 23, "current_month": 6, "email_sent": False}
        expected = 'email not sent'
        self.assert_check_emailer(todays_date, flowermap, expected)
    
    def test_check_emailer3(self):
        todays_date = datetime.date(2013,6,13)
        flowermap = {"flowerday": 23, "current_month": 6, "email_sent": False}
        expected = 'email not sent'
        self.assert_check_emailer(todays_date, flowermap, expected)

    def test_check_emailer4(self):
        todays_date = datetime.date(2013,6,23)
        flowermap = {"flowerday": 23, "current_month": 6, "email_sent": False}
        expected = 'email sent'
        self.assert_check_emailer(todays_date, flowermap, expected)

    def test_check_emailer4(self):
        todays_date = datetime.date(2013,5,23)
        flowermap = {"flowerday": 23, "current_month": 6, "email_sent": True}
        expected = 'email not sent'
        self.assert_check_emailer(todays_date, flowermap, expected)

    def assert_check_emailer(self, todays_date, flowermap, expected):
        def test_email_chris(flowermap, todays_date):
            return flowermap, todays_date
        email_status = flowers.check_date_for_emailer(flowermap, todays_date, test_email_chris(flowermap, todays_date))
        self.assertEquals(email_status, expected)

if __name__ == '__main__':
    unittest.main()