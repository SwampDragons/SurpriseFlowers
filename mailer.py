"""Send email, managing all details such as authentication."""
import smtplib

username = 'none'
password = 'none'

try:
    import settings
    username = settings.USERNAME
    password = settings.PASSWORD
    fromaddr = settings.FROMADDR
    toaddr = settings.TOADDR
    msg = settings.EMAIL_MESSAGE
except ImportError:
    pass


def send_email():
    """Generate and send email."""
    return

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddr, msg)
    except smtplib.SMTPAuthenticationError as e:
        print e
    finally:
        server.quit()
