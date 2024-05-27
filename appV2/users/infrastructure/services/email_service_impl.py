import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings import EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_FROM

from appV2.users.domain.services.email_service import EmailService
from appV2.users.application.exceptions.user_exceptions import EmailError

class EmailServiceImpl(EmailService):
    
    def send_email(self,
             to: list[str],
             subject: str,
             body: str) -> bool:

        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = ', '.join(to)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, to, msg.as_string())
            print('APP INFO: Email sended to: ' + ', '.join(to))
            return True
        except Exception as e:
            print(e)
            raise EmailError()