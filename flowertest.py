# This is the tests for the flower program!!
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
    def test_date_checker_no_file(self):
        if os.path.isfile(flowers.filename):
            os.remove(flowers.filename)
    def test_date_checker_file_from_last_month(self):
        pass
    def test_date_checker_file_from_this_month_saved_day_is_before_today(self):
        pass
    def test_date_checker_file_from_this_month_saved_day_is_today(self):
        pass
    def test_date_checker_file_from_this_month_saved_day_is_after_today(self):

if __name__ == '__main__':
    unittest.main()

# def test_date_checker():
#     test_flowermap = {'flowerday':flowerday, "last_email": "2013-05-26 15:56:04.273416", 'last_gen_month':'5'}
#     # test date_checker with day = first of month
#     first_day = datetime.datetime(2013, 6, 1, 17, 13, 26, 812111)
#     date_checker(first_day)
#     with open(filename, 'w') as f:
#         flowermap = json.loads(f.read())
#     if flowermap['flowerday']:

#     # test date_checker with day = random day not the same as the day in file
#     test_day = datetime.datetime(2013, 6, 2, 17, 13, 26, 812111)
#     # test date when today shouldbe the day!
#     # set file so that flowerday is not rand_day
#     format: flowermap = {"flowerday": 26, "last_email": "2013-05-26 15:56:04.273416"}
#     with open(filename, 'w') as f:
#         flowermap = json.loads(f.read())

#     # need to set file so that flowerday is rand_day
#     format: flowermap = {"flowerday": 2, "last_email": "2013-05-26 15:56:04.273416"}
#     with open(filename, 'w') as f:
#         flowermap = json.loads(f.read())