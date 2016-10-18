"""Configure SurpriseFlowers."""

from datetime import datetime
import json
import os
from crontab import CronTab
import flowers

#  @hourly python /Users/mmarsh/Projects/SurpriseFlowers/flowers.py

PROJECT_ROOT = os.path.abspath(os.path.dirname("__file__"))


def append_to_crontab():
    """
    Add cron task to run flowers.py hourly.

    Adds the following line to your CronTab
    @hourly python /Path/To/Repo/SurpriseFlowers/flowers.py
    """
    flowerfile = os.path.join(PROJECT_ROOT, "flowers.py")
    if not os.path.isfile(flowerfile):
        print """
              Something is wrong with your repo structure;
              flowers.py should be in the same directory as this setup file.

              Unable to create crontab for you; please manually update the
              crontab accordring to the example in the readme.
              """
        return

    # gets your user cron
    cron = CronTab(user=True)
    job = cron.new(command="python %s" % flowerfile)
    job.every().hour()
    cron.write()


def generate_settings_file():
    """Interactively generate email settings file."""
    # TODO extend so that person buying flowers can install it on their
    # computer without confusion.
    username = raw_input("What is your email username?")
    password = raw_input("What is your email password?")
    fromaddr = raw_input("What is your email address?")
    floweree_name = raw_input("What is your name?")
    flowerer_name = raw_input("What is your loved one's name?")
    toaddr = raw_input("What is your loved one's email address?")
    gift = raw_input("What is the small token of love you want to be reminded",
                     "to send? (default: flowers")
    email_message = """
        Subject: Surprise {0}\n\n
        Hey {1},\n
        You really care about {2} and we both know they'd love to be reminded
        of that. You know how you could remind {2}? How about getting them a
        gift of {0} just because?\n\n

        Love,\n
        SurpriseFlowersBot
        """.format(gift, flowerer_name, floweree_name)

    settings = {"username": username,
                "password": password,
                "fromaddr": fromaddr,
                "toaddr": toaddr,
                "gift": gift,
                "email_message": email_message}

    with open("email_settings.py", "w") as f:
        f.write(json.dumps(settings))


def main():
    """Configure, create settings and crontab, and then run for first time."""
    generate_settings_file()
    append_to_crontab()
    # run flowers program for first time based on new settings.
    flowers.run(datetime.datetime.today())


if __name__ == "__main__":
    main()
