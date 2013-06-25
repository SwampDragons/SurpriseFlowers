# This program exists to remind Chris to buy me flowers "just because" on a monthly basis.  
# It is called by the following cron job once per day:
# 0 0 1  * * /usr/local/bin/python /Users/mmarsh/Projects/SurpriseFlowers/flowers.py
#
# next steps:
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
    # This function picks a random day of the current month and saves it to flowermap

    # generate a random integer from 1 : the number of days in the month
    _, ndays = calendar.monthrange(todays_date.year, todays_date.month)
    flowerday = random.choice(range(1,ndays+1))
    # print 'flowerday is...',flowerday
    recentmonth = todays_date.month
    # print 'recent month is...', recentmonth
    flowermap = {'flowerday':flowerday, 'current_month':recentmonth, 'email_sent':False}
    with open(filename, 'w') as f:
        f.write(json.dumps(flowermap))
        # add todays_date to flowerdates.txt
    return flowermap

def email_chris(flowermap, todays_date):
    # This function creates and sends the email, using smtplib
    #email_subject = "Subject: Surprise Flowers!\n\n"
    # msg['Subject'] = 'The contents of %s' % textfile
    # msg['From'] = me
    # msg['To'] = you

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

    # with open(os.path.join(PROJECT_ROOT,'temp.txt'), 'a') as f:
        # f.write('\n email Chris {0}'.format(datetime.datetime.now()))
    with open(filename, 'w') as f:
        flowermap['flowerday'] = todays_date.day
        flowermap['current_month'] = todays_date.month
        flowermap['email_sent'] = True
        f.write(json.dumps(flowermap))

def check_file(filename):
    # This function reads flowermap from the save fie; 
    # if no save file exists then this function creates the file for the first time  

    file_status = '-1'

    if not os.path.isfile(filename):
        # print 'creating flowerdate.txt...'
        flowermap = {'flowerday':None, 'current_month':None, 'email_sent':False}
        # print flowermap
        with open(filename, 'w') as f:
            f.write(json.dumps(flowermap))
        file_status = 'created file'

    # file already exists, so read it
    else:  
        with open(filename, 'r') as f:
            flowermap = json.loads(f.read())     
        file_status = 'read file' 

    # return the contents of the file
    return flowermap, file_status
    
def check_date_for_emailer(flowermap, todays_date, callback):
    # This function determines based on flowermap whether it is time to send the email

    email_status = 'email not sent'

    # if today's date matches this month's generated date, run emailer
    if flowermap['flowerday'] <= todays_date.day and \
    flowermap['current_month'] == todays_date.month and flowermap['email_sent'] == False:
        email_status = 'email sent'
        callback(flowermap, todays_date)

    return email_status

def check_date_for_generator(flowermap, todays_date): 
    #This function determines whether it is time to generate a new random day of the month

    generator_status = 'date not generated'

    # if today is the first day of the month
    # or the first time we ran the program this month pick a random day of the month to buy flowers for me.
    if (todays_date.day >= 1 and flowermap['current_month'] < todays_date.month) or \
            flowermap['flowerday'] == None:

        generator_status = 'date was generated'
        flowermap = date_generator(todays_date)

    return flowermap, generator_status

def main(todays_date, callback):
    # if no save file existed before today, initialize the flowermap variable and save it to a file
    flowermap, file_status = check_file(filename)

    # in no file existed before today, generate a legitimate date
    flowermap, generator_status = check_date_for_generator(flowermap, todays_date)

    # check whether we should email the person
    email_status = check_date_for_emailer(flowermap, todays_date, callback)

if __name__ == '__main__':
    main(datetime.date.today(), email_chris)



