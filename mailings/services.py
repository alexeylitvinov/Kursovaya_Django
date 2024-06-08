from django.core.mail import send_mass_mail

from config.settings import EMAIL_HOST_USER
from mailings.models import Mail
from users.models import Client


def send_email_to_all_clients(request, mail_slug):
    mail_object = Mail.objects.get(slug=mail_slug)
    clients = Client.objects.filter(user=request.user)
    client_emails = [client.email for client in clients if client.email]
    messages = [
        (
            mail_object.subject,
            mail_object.body,
            EMAIL_HOST_USER,
            [email]
        )
        for email in client_emails
    ]
    send_mass_mail(tuple(messages), fail_silently=False)
