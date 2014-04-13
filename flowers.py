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
    import email_config
    username = email_config.USERNAME
    password = email_config.PASSWORD
    fromaddr = email_config.FROMADDR
    toaddr = email_config.TOADDR
    flower_sender_name = email_config.SENDERNAME
    flower_recipient_name = email_config.RECIPIENTNAME
except ImportError:
    raise Warning("could not find local email_config")

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
filename = os.path.join(PROJECT_ROOT, 'flowerdate.txt')

class SurpriseFlowers(object):

    def __init__(self, date=None, flowermap=None):
        self.date = date
        self.flowermap = flowermap
        if not self.date:
            self.date = datetime.date.today()
        if not self.flowermap:
            self.flowermap = {}


    def date_generator(self):
        # generate a random integer from 1 : the number of days in the month
        _, ndays = calendar.monthrange(self.date.year, self.date.month)
        flowerday = random.choice(range(1,ndays+1))
        # print 'flowerday is...',flowerday
        recentmonth = self.date.month
        # print 'recent month is...', recentmonth
        self.flowermap = {'flowerday':flowerday, 'current_month':recentmonth, 'email_sent':False}
        with open(filename, 'w') as f:
            f.write(json.dumps(self.flowermap))
            # add self.date to flowerdates.txt
        return self.flowermap

    def send_email(self):
        # This function creates and sends the email, using smtplib
        # email_subject = "Subject: Surprise Flowers!\n\n"
        # msg['Subject'] = 'The contents of %s' % textfile
        # msg['From'] = me
        # msg['To'] = you

        msg = """Subject: Surprise Flowers!\n\n
        {0} is great.\n
        I love {0}.\n
        You know how I can tell {0} that {0} is great?  FLOWERS!\n
        I should buy {0} flowers."""
        msg.format(RECIPIENTNAME)

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
            self.flowermap['flowerday'] = self.date.day
            self.flowermap['current_month'] = self.date.month
            self.flowermap['email_sent'] = True
            f.write(json.dumps(self.flowermap))

    def check_file(filename):
        # This function reads self.flowermap from the save fie;
        # if no save file exists then this function creates the file for the first time

        file_status = '-1'

        if not os.path.isfile(filename):
            # print 'creating flowerdate.txt...'
            self.flowermap = {'flowerday':None, 'current_month':None, 'email_sent':False}
            # print self.flowermap
            with open(filename, 'w') as f:
                f.write(json.dumps(self.flowermap))
            file_status = 'created file'

        # file already exists, so read it
        else:
            with open(filename, 'r') as f:
                self.flowermap = json.loads(f.read())
                # print self.flowermap
            file_status = 'read file'

        # return the contents of the file
        return self.flowermap, file_status

    def check_date_for_emailer(self, callback):
        # This function determines based on self.flowermap whether it is time to send the email

        email_status = 'email not sent'
        # if today's date matches this month's generated date, run emailer
        if self.flowermap['flowerday'] <= self.date.day and \
        self.flowermap['current_month'] == self.date.month and self.flowermap['email_sent'] == False:
            email_status = 'email sent'
            callback(self.flowermap, self.date)

        return email_status

    def check_date_for_generator(self):
        #This function determines whether it is time to generate a new random day of the month

        generator_status = 'date not generated'

        if ((self.date.day >= 1 and
            (self.flowermap['current_month'] < self.date.month) or
            self.flowermap['current_month'] == 12 and self.date.month == 1) or
                self.flowermap['flowerday'] == None):
            generator_status = 'date was generated'
            self.flowermap = self.date_generator()
        # print generator_status
        return self.flowermap, generator_status

def main(self, callback):
    # if no save file existed before today, initialize the self.flowermap variable and save it to a file
    self.flowermap, file_status = check_file(filename)

    # in no file existed before today, generate a legitimate date
    self.flowermap, generator_status = check_date_for_generator(self.flowermap, self.date)

    # check whether we should email the person
    email_status = check_date_for_emailer(self.flowermap, self.date, callback)

if __name__ == '__main__':
    main(datetime.date.today(), send_email)



