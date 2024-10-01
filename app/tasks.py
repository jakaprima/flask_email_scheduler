from celery import current_app as celery
from .models import Email
from flask_mail import Message
from .extensions import mail

@celery.task
def long_task(n):
    """A long-running task."""
    print("celery", celery)
    import time
    time.sleep(n)
    return f"Task completed after {n} seconds!"

@celery.task
def send_mail_task(mail_id):
    email = Email.query.get(mail_id)
    if email:
        msg = Message(email.email_subject, recipients=['jakaprima123@gmail.com'])  # Replace with actual recipient
        msg.body = email.email_content
        msg.charset = 'UTF-8'
        mail.send(msg)

    return f"Task completed {email} sent!"
