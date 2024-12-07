import os
import random
from dotenv import load_dotenv
load_dotenv()

from django.core.mail import send_mail
from django.core.cache import cache

from config.celery import app


@app.task(bind=True, ignore_result=True)
def send_email_code(self, email, subject):
    code = random.randint(1000, 9999)
    cache.set(str(email), code, 240)
    send_mail(
        subject=subject,
        message=f"Your activation code is {code},  code life time 4 min",
        from_email=os.getenv("SENDER_EMAIL"),
        recipient_list=[email, ]
    )
    print(code)


@app.task(bind=True, ignore_result=True)
def send_forgot_password_code(self, email, subject, new_password):
    send_mail(
        subject=subject,
        message=f"Your new password  is: {new_password}",
        from_email=os.getenv("SENDER_EMAIL"),
        recipient_list=[email, ]
    )
    print(new_password)
