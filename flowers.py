# This program exists to remind Chris to buy me flowers "just because" on a monthly basis.  
# It is called by the following cron job once per day:
# 0 0 1  * * /usr/local/bin/python /Users/mmarsh/Projects/SurpriseFlowers/flowers.py
#
# eventual features:
#   1. Have option to select frequency of flowers (e.g. every two weeks or bimonthly)
#   2. Send additional reminders for birthdays, anniversaries, 
#      and holidays where flowers are expected
#   3. post event to google calendar with reminder for flowers
#
import datetime
import calendar
import random
import os
import smtplib
import json

username = 'none'
password = 'none'

try:
    import local_settings as settings
    username = settings.USERNAME
    password = settings.PASSWORD
    fromaddr = settings.FROMADDR
    toaddr = settings.TOADDR 
except ImportError:
    pass

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
filename = os.path.join(PROJECT_ROOT, 'flowerdate.txt')

def date_generator(todays_date):
    # generate a random integer from 1 : the number of days in the month
    _, ndays = calendar.monthrange(todays_date.year, todays_date.month)
    flowerday = random.choice(range(1,ndays+1))
    print 'flowerday is...',flowerday
    recentmonth = todays_date.month
    print 'recent month is...', recentmonth
    flowermap = {'flowerday':flowerday, 'current_month':recentmonth, 'email_sent':False}
    with open(filename, 'w') as f:
        f.write(json.dumps(flowermap))
        # add todays_date to flowerdates.txt
    return flowermap

def email_chris(flowermap, todays_date):
    msg = """Subject: Surprise Flowers!\n\n
    Megan is great.\n
    I love Megan.\n
    You know how I can tell her she's great?  FLOWERS!\n
    I should buy her flowers."""

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddr, msg)
    except smtplib.SMTPAuthenticationError as e:
        print e
    finally:
        server.quit()

    with open(os.path.join(PROJECT_ROOT,'temp.txt'), 'a') as f:
        f.write('\n email Chris {0}'.format(datetime.datetime.now()))
    with open(filename, 'w') as f:
        flowermap['flowerday'] = todays_date.day
        flowermap['current_month'] = todays_date.month
        flowermap['email_sent'] = True
        f.write(json.dumps(flowermap))

def date_checker(todays_date):
    if not os.path.isfile(filename):
        print 'creating flowerdate.txt...'
        # create the file for the first time, since it doesn't exist!
        flowermap = {'flowerday':None, 'current_month':None, 'email_sent':False}
        print flowermap
        with open(filename, 'w') as f:
            f.write(json.dumps(flowermap))
        flowermap = date_generator(todays_date)
    
    # open the file and read the values!
    with open(filename, 'r') as f:
        flowermap = json.loads(f.read())
    
    if todays_date.day >= 1 and flowermap['current_month'] < todays_date.month:
        print 'today is the first of the month! (or the first time we ran the program this month)'
        # if today is the first day of the month, pick a random day of the month to buy flowers for me.
        date_generator(todays_date)
    # send_email:
    else flowermap['flowerday'] <= todays_date.day and \
    flowermap['current_month'] == todays_date.month and flowermap['email_sent'] == False:
        # if today's date matches this month's generated date, run emailer
        print 'emailing...'
        email_chris(flowermap, todays_date)

if __name__ == '__main__':
    date_checker(datetime.date.today())

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



