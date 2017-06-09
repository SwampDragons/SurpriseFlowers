# Surprise Flowers
This little tool traces its origins to a joke-argument between my husband and
me about four years ago, when I was first learning Python. The premise of the
argument was that while he bought me flowers on all of the important special
occasions -- e.g. my birthday, our anniversary, Valentine's Day -- he never
bought me flowers "just because." His defense was that since he loved me so
much _all the time_ he never thought "I love her so much right now that
I'm going to buy her flowers."

I said, "I think I can fix that," and Surprise Flowers was born.

The tool is simple.  It is intended to be run as a cron task on a computer you
use fairly frequently.  It picks a random day of the month to email your
significant other (or, you can set it up to run for yourself!) and on that
day will email a "buy flowers" reminder.

## Dependencies
You need to have a gmail account which you've gotten an application password
for.  Also you need to be able to setup a crontab.  I've only tested this on my
mac, so you need one of those or, I imagine, a linux machine.  I haven't
tried running this on Windows.

## Setup
You can either use my seutp script or set up yourself.
### Setup Script
from the repo directory, run
```
python setup.py
```
and follow the instructions in the prompts.

### Manual
Get an application password from your mac.
Clone the repo:
```
git clone git@github.com:SwampDragons/SurpriseFlowers.py
cd SurpriseFlowers
touch settings.py
```

Then open the settings file and copy this code into it:
```python
#!/usr/bin/env python
# encoding: utf-8
"""Local settings not to be shared with github."""
USERNAME = "youremail@gmail.com"
PASSWORD = "super-secret-password-from-google"
FROMADDR = "youremail@gmail.com"
TOADDR = "flower-recipient@email.com"
EMAIL_MESSAGE = """Subject: Surprise Flowers!\n\n
    <Flower Recipient> is great.\n
    I love <Flower Recipient>.\n
    You know how I can tell them they're great?  FLOWERS!\n
    I should buy them flowers."""
```
Open your crontab to edit it:
`crontab -e`

Add something like this:
```
@hourly python /my/repo/dir/SurpriseFlowers/flowers.py
```