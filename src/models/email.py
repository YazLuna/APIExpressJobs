"""This module manages the sending of messages to the email."""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.routes.responses_rest import ResponsesREST


class Email:
    """This class manages the sending of messages to the email."""

    @staticmethod
    def send_email(email, message_send):
        """This function sends the verification code to an email."""
        result = ResponsesREST.SERVER_ERROR.value
        msg = MIMEMultipart()

        message = "Su código de verificación es: " + str(message_send)

        password = "expressjobsMmolYalh"
        msg['From'] = "expressjobsapp@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Mensaje de la aplicación de TrabajosExprés"

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com: 587')

        server.starttls()

        server.login(msg['From'], password)

        server.sendmail(msg['From'], msg['To'], msg.as_string())

        server.quit()

        result = ResponsesREST.CREATED.value
        return result

    @staticmethod
    def send_message_email(message_send, email):
        """This function sends a message to an email."""
        result = ResponsesREST.SERVER_ERROR.value
        msg = MIMEMultipart()

        message = str(message_send)

        password = "expressjobsMmolYalh"
        msg['From'] = "expressjobsapp@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Mensaje de la aplicación de TrabajosExprés"

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com: 587')

        server.starttls()

        server.login(msg['From'], password)

        server.sendmail(msg['From'], msg['To'], msg.as_string())

        server.quit()

        result = ResponsesREST.CREATED.value
        return result
