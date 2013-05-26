# This program exists to remind Chris to buy me flowers "just because" on a monthly basis.  
# eventual features to add once main program runs:
# It is called by the following cron job once per day:
# 0 0 1  * * /usr/local/bin/python /Users/mmarsh/Projects/SurpriseFlowers/flowers.py
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
    return flowerday

def email_chris(flowermap):
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
        flowermap['last_email'] = str(datetime.datetime.now())
        f.write(json.dumps(flowermap))

def date_checker():
    # Get today's date
    todays_date = datetime.date.today()
    # if today is the first day of the month, pick a random day of the month to buy flowers for me.
    if todays_date.day == 1 or not os.path.isfile(filename):
        flowerday = date_generator(todays_date)
        # save this date to a text file for future access
        flowermap = {'flowerday':flowerday, 'last_email':None}
        with open(filename, 'w') as f:
            f.write(json.dumps(flowermap))
            # add todays_date to flowerdates.txt
    else:
        with open(filename, 'r') as f:
            flowermap = json.loads(f.read())
            if flowermap['last_email']:
                flowermap['last_email'] = datetime.datetime.strptime(flowermap['last_email'], '%Y-%m-%d %H:%M:%S.%f')
    if flowermap['flowerday'] <= todays_date.day and \
            (not flowermap['last_email'] or todays_date.month > flowermap['last_email'].month):
        # if today's date matches this month's generated date, run emailer
        email_chris(flowermap)

if __name__ == '__main__':
    date_checker()
