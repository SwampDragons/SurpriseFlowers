# This is the tests for the flower program!!
import datetime
import json
import os
import unittest
import flowers

## test the method to create a file if it isn't present
#class FlowerTest(unittest.TestCase):
#
#    def test_check_file_present(self):
#        expected = {"flowerday": 20, "current_month": 6, "email_sent": True}
#        with open(flowers.filename, 'w') as f:
#            f.write(json.dumps(expected))
#        flowermap, file_status = flowers.check_file(flowers.filename)
#        self.assertEquals(flowermap,expected)
#        os.remove(flowers.filename)
#
#    def test_check_file_absent(self):
#        if os.path.isfile(flowers.filename):
#            os.remove(flowers.filename)
#
#        expected = {'flowerday':None, 'current_month':None, 'email_sent':False}
#        flowermap, file_status = flowers.check_file(flowers.filename)
#        self.assertEquals(flowermap, expected)
#
#        with open(flowers.filename, 'r') as f:
#            flowermap = json.loads(f.read())
#        self.assertEquals(flowermap, expected)

class TestSurpriseFlowers(unittest.TestCase):

    def setUp(self):
        self.cls = flowers.SurpriseFlowers

    def test_check_date_for_emailer(self):
        def test_email_chris(flowermap, todays_date):
            return flowermap, todays_date
            # test the method that checks to see if it should send an email
        run_conditions = [[{"flowerday": 23, "current_month": 6, "email_sent": True}, 'email not sent', datetime.date(2013,6,24)],
                      [{"flowerday": 23, "current_month": 6, "email_sent": False}, 'email not sent', datetime.date(2013,6,13)],
                      [{"flowerday": 23, "current_month": 6, "email_sent": False}, 'email not sent', datetime.date(2013,6,13)],
                      [{"flowerday": 23, "current_month": 6, "email_sent": False}, 'email sent', datetime.date(2013,6,23)],
                      [{"flowerday": 23, "current_month": 6, "email_sent": True}, 'email not sent', datetime.date(2013,5,23)],
                      [{"flowerday": 23, "current_month": 6, "email_sent": False}, 'email not sent', datetime.date(2013,5,23)]]
        for flowermap, expected, todays_date in run_conditions:
            email_status = self.cls(flowermap=flowermap, date=todays_date).check_date_for_emailer(test_email_chris)
            self.assertEquals(email_status, expected)

    def test_check_date_for_generator(self):
        self.todays_date = datetime.date(2013,6,23)
        run_conditions = [[{"flowerday": 23, "current_month": 6, "email_sent": False}, 'date not generated'],
                      [{"flowerday": 24, "current_month": 6, "email_sent": True}, 'date not generated'],
                      [{"flowerday": 23, "current_month": 5, "email_sent": False}, 'date was generated']]

        for flowermap, expected in run_conditions:
            flowermap, generator_status = self.cls(flowermap=flowermap, date=self.todays_date).check_date_for_generator()
            self.assertEquals(generator_status, expected)


if __name__ == '__main__':
    unittest.main()