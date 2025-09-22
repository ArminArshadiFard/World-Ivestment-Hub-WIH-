from django.core.management.base import BaseCommand
from account.models import ValidationCode
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from WIH import settings

fromaddr = settings.EMAIL_HOST_USER
smtp_server = 'mail.w-i-h.com'
port = 465


class Command(BaseCommand):
    help = "send_email"

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **options):
        server = smtplib.SMTP_SSL(smtp_server, port)
        server.login(fromaddr, settings.EMAIL_HOST_PASSWORD)
        while True:
            try:
                time.sleep(8)
                validation_list = ValidationCode.objects.filter(send_email_status=0)
                for i in validation_list:
                    html_content = f'<h1 style="text-align: center;color: forestgreen;padding-top: 150px">Thanks for registration in wi-hub.com</h1><h2 style="text-align: center;color: forestgreen">take the code to verify your account </h2><h2 style="text-align: center;color: red">{i.code}</h2>'
                    toaddr = i.user.username
                    msg = MIMEMultipart()
                    msg['From'] = fromaddr
                    msg['To'] = toaddr
                    msg['Subject'] = "Activation Code"
                    msg.attach(MIMEText(html_content, "html"))
                    text = msg.as_string()
                    server.sendmail(fromaddr, toaddr, text)
                    i.send_email_status = 1
                    i.save()
            except Exception as e:
                print("error: ", e)
                server = smtplib.SMTP_SSL(smtp_server, port)
                server.login(fromaddr, settings.EMAIL_HOST_PASSWORD)
