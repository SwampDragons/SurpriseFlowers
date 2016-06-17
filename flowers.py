"""
Send email to a loved one to encourage them to make a small gesture of love.

Run this code as a once-daily cron task.  It will randomly pick a day of the
month to send an email to your loved one, telling them to buy you flowers.
"""

import datetime
import calendar
import random
import os
import json

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
filename = os.path.join(PROJECT_ROOT, 'flowerdate.txt')


def load_or_create_flowermap(filename):
    """Read flowermap file if it exists; generate flowermap if it does not."""

    if not os.path.isfile(filename):
        flowermap = {'flowerday': None,
                     'current_month': None,
                     'email_sent': False}

        with open(filename, 'w') as f:
            f.write(json.dumps(flowermap))

    # file already exists, so read it
    else:
        with open(filename, 'r') as f:
            flowermap = json.loads(f.read())

    return flowermap


def update_flowermap(flowermap, todays_date):
    with open(filename, 'w') as f:
        flowermap['flowerday'] = todays_date.day
        flowermap['current_month'] = todays_date.month
        flowermap['email_sent'] = True
        f.write(json.dumps(flowermap))


def check_date_for_emailer(flowermap, todays_date):
    """Use flowermap to figure out if today is the day to send the email."""

    email_status = 'email not sent'

    # if today's date matches this month's generated date, run emailer
    if flowermap['flowerday'] <= todays_date.day and \
            flowermap['current_month'] == todays_date.month and
            flowermap['email_sent'] == False:
        email_status = 'email sent'
        send_email()
        update_flowermap(flowermap, todays_date)

    return email_status


def generate_date(flowermap, todays_date):
    """Check whether we should generate a new date; if so, run generator."""

    date_generated = False

    if (todays_date.day >= 1 and flowermap['current_month'] < todays_date.month) or \
            flowermap['flowerday'] == None:

        date_generated = True

        _, ndays = calendar.monthrange(todays_date.year, todays_date.month)
        flowerday = random.choice(range(1, ndays + 1))
        # print 'flowerday is...',flowerday
        recentmonth = todays_date.month
        # print 'recent month is...', recentmonth
        flowermap = {'flowerday': flowerday, 'current_month': recentmonth, 'email_sent': False}
        with open(filename, 'w') as f:
            f.write(json.dumps(flowermap))
            # add todays_date to flowerdates.txt

    return flowermap


def main(todays_date):
    flowermap = load_or_create_flowermap(filename)

    flowermap = generate_date(flowermap, todays_date)

    # check whether we should email the person
    email_status = check_date_for_emailer(flowermap, todays_date)


if __name__ == '__main__':
    main(datetime.date.today())



