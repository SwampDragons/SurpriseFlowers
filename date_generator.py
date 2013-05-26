# This program exists to remind Chris to buy me flowers "just because" on a monthly basis.  
# eventual features to add once main program runs:
#
#   1. Have option to select frequency of flowers (e.g. every two weeks or bimonthly)
#   2. Send additional reminders for birthdays, anniversaries, 
#      and holidays where flowers are expected
#   3. post event to google calendar with reminder for flowers
#
import datetime
import calendar
import random
import os
filename = 'flowerdate.txt'

def date_generator(todays_date):
    # generate a random integer from 1 : the number of days in the month
    _, ndays = calendar.monthrange(todays_date.year, todays_date.month)
    flowerday = random.choice(range(1,ndays+1))
    return flowerday
    # check whether that day of the month is a weekday or a weekend
    # if weekday, email Chris at 4pm
    # if weekend, email Chris at 10am

def email_chris():
    with open('temp.txt', 'a') as f:
        f.write('\n email Chris {0}'.format(datetime.datetime.now()))

def date_checker():
    # Get today's date
    todays_date = datetime.date.today()
    # if today is the first day of the month, pick a random day of the month to buy flowers for me.
    if todays_date.day == 1 or not os.path.isfile(filename):
        flowerday = date_generator(todays_date)
        # save this date to a text file for future access
        with open(filename, 'w') as f:
            f.write(str(flowerday))
            # add todays_date to flowerdates.txt
    else:
        with open(filename, 'r') as f:
            flowerday = int(f.read())
    if flowerday == todays_date.day:
        # if today's date matches this month's generated date, run emailer
        email_chris()

if __name__ == '__main__':
    date_checker()
