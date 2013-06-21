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

def check_file(filename):
    if not os.path.isfile(filename):
        print 'creating flowerdate.txt...'
        # create the file for the first time, since it doesn't exist!
        flowermap = {'flowerday':None, 'current_month':None, 'email_sent':False}
        print flowermap
        with open(filename, 'w') as f:
            f.write(json.dumps(flowermap))
    else:  
        with open(filename, 'r') as f:
            flowermap = json.loads(f.read())      
    return flowermap
    
def date_checker(todays_date):
    flowermap = check_file(filename)
    
    if flowermap['flowerday'] == None:
        flowermap = date_generator(todays_date)
    
    if todays_date.day >= 1 and flowermap['current_month'] < todays_date.month:
        print 'today is the first of the month! (or the first time we ran the program this month)'
        # if today is the first day of the month, pick a random day of the month to buy flowers for me.
        date_generator(todays_date)
    # send_email:
    elif flowermap['flowerday'] <= todays_date.day and \
    flowermap['current_month'] == todays_date.month and flowermap['email_sent'] == False:
        # if today's date matches this month's generated date, run emailer
        print 'emailing...'
        email_chris(flowermap, todays_date)

if __name__ == '__main__':
    date_checker(datetime.date.today())



