from django.core.mail import send_mail

import uuid
from django.conf import settings


def send_forgot_email(email,token):
    
    subject='your password is'
    message=f'hi your pass link is http://127.0.0.1:9000/change-password/{token}/'
    email_from='bharattechdotorg@gmail.com'
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
    return True


def send_otp_email(email,otp):
    
    subject='your password is'
    message=f'hi your otp is: {otp}'
    email_from='bharattechdotorg@gmail.com'
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
    return True