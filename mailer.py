#!/usr/bin/env python
# encoding: utf-8
"""Send email, managing all details such as authentication."""
import smtplib

username = None
password = None

try:
    import settings
    username = settings.USERNAME
    password = settings.PASSWORD
    fromaddr = settings.FROMADDR
    toaddr = settings.TOADDR
    msg = settings.EMAIL_MESSAGE
except ImportError as e:
    raise("COULDNT IMPORT LOCAL SETTINGS: %s" % e)


def send_email():
    """Generate and send email."""

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, password)
        server.sendmail(fromaddr, toaddr, msg)
    except Exception as e:
        raise e
    finally:
        server.quit()
