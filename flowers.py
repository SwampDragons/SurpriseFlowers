#!/usr/bin/env python
# encoding: utf-8
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
from mailer import send_email

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
FLOWERDATE_FILE = os.path.join(PROJECT_ROOT, 'flowerdate.json')


def write_flowermap(day, month, email_sent):
    flowermap = {'flowerday': day,
                 'current_month': month,
                 'email_sent': email_sent}

    with open(FLOWERDATE_FILE, 'w') as f:
        f.write(json.dumps(flowermap))

    return flowermap


def load_or_create_flowermap():
    """Read flowermap file if it exists; generate flowermap if it does not."""

    if not os.path.isfile(FLOWERDATE_FILE):
        flowermap = write_flowermap(None, None, False)
    else:
        with open(FLOWERDATE_FILE, 'r') as f:
            flowermap = json.loads(f.read())

    return flowermap


def check_date_for_emailer(flowermap, todays_date):
    """Use flowermap to figure out if today is the day to send the email."""

    email_sent = False

    # if today's date matches this month's generated date, run emailer
    if flowermap['flowerday'] <= todays_date.day and \
            flowermap['current_month'] == todays_date.month and \
            not flowermap['email_sent']:
        email_sent = True
        send_email()
        write_flowermap(todays_date.day, todays_date.month, email_sent)

    return email_sent


def generate_date(flowermap, todays_date):
    """Check whether we should generate a new date; if so, run generator."""

    if not flowermap['flowerday'] or flowermap['current_month'] != todays_date.month:

        _, ndays = calendar.monthrange(todays_date.year, todays_date.month)
        flowerday = random.choice(range(1, ndays + 1))
        # print 'flowerday is...',flowerday
        recentmonth = todays_date.month
        # print 'recent month is...', recentmonth
        flowermap = write_flowermap(flowerday, recentmonth, False)

    return flowermap


def main(todays_date):
    flowermap = load_or_create_flowermap()
    flowermap = generate_date(flowermap, todays_date)
    check_date_for_emailer(flowermap, todays_date)


if __name__ == '__main__':
    main(datetime.date.today())
