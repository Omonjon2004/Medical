import os
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(email, confirmation_code):
    send_mail(
        'Registration Confirmation Code',
        f'Your confirmation code is: {confirmation_code}',
        'from@example.com',
        [email],
        fail_silently=False,
    )

    return "Done"


@shared_task(bind=True, ignore_result=True)
def send_forgot_password_code(self, email, subject, new_password):
    send_mail(
        subject=subject,
        message=f"Your new password is: {new_password}",
        from_email=os.getenv("SENDER_EMAIL"),
        recipient_list=[email],
    )