from celery import shared_task
from mail_templated import EmailMessage




@shared_task
def send_email_with_celery(template:str, token:str, sender:str, receiver:list):
    message = EmailMessage(
                template,
                {"token": token},
                sender,
                to=receiver,
            )
    message.send()
