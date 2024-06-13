from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from smtplib import SMTPException

from apscheduler.schedulers.background import BackgroundScheduler
from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, MailingAttempt
from users.models import Client


def send_email_to_all_clients(mailing):
    """Функция отправки писем клиентам"""
    clients = Client.objects.filter(user=mailing.mail.user)
    for client in clients:
        try:
            send_mail(
                subject=mailing.mail.subject,
                message=mailing.mail.body,
                from_email=EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False
            )
            MailingAttempt.objects.create(
                mailing=mailing,
                client=client,
                last_attempt_date=timezone.now(),
                status=MailingAttempt.AttemptStatusChoices.SUCCESS,
                server_response='Письмо успешно отправлено'
            )
        except SMTPException as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                client=client,
                last_attempt_date=timezone.now(),
                status=MailingAttempt.AttemptStatusChoices.FAILURE,
                server_response=str(e)
            )


def schedule_mailing_tasks():
    """Функция запуска планировщика задач"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_send_mailings, 'interval', minutes=1)  # Проверка каждую минуту
    scheduler.start()
    print('Планировщик запущен')


def change_mailing_status(request, pk):
    """Функция изменения статуса рассылки"""
    mailing_object = Mailing.objects.get(id=pk)
    mailing_object.status = 'R'
    mailing_object.save()
    return HttpResponseRedirect(reverse('mailings:mails'))


def check_and_send_mailings():
    """Функция для проверки и отправки писем"""
    current_time = timezone.localtime(timezone.now())
    mailings_to_send = Mailing.objects.filter(
        first_send_date__lte=current_time.date(),
        send_time__lte=current_time.time(),
        status=Mailing.StatusChoices.RUNNING
    )
    for mailing in mailings_to_send:
        last_successful_attempt = MailingAttempt.objects.filter(
            mailing=mailing,
            status=MailingAttempt.AttemptStatusChoices.SUCCESS
        ).order_by('-last_attempt_date').first()
        if should_send_now(mailing, current_time, last_successful_attempt):
            send_email_to_all_clients(mailing)


def should_send_now(mailing, current_time, last_successful_attempt):
    """Функция определяет, следует ли отправлять рассылку в данный момент"""
    if last_successful_attempt and last_successful_attempt.last_attempt_date.date() == current_time.date():
        return False
    if current_time.time() >= mailing.send_time:
        if mailing.frequency == Mailing.FrequencyChoices.DAILY:
            return True
        elif mailing.frequency == Mailing.FrequencyChoices.WEEKLY:
            first_send_day_of_week = mailing.first_send_date.weekday()
            return current_time.weekday() == first_send_day_of_week
        elif mailing.frequency == Mailing.FrequencyChoices.MONTHLY:
            first_send_day_of_month = mailing.first_send_date.day
            return current_time.day == first_send_day_of_month
    return False


def complete_mailing(request, pk):
    """Функция меняет статус рассылки на Завершена"""
    mailing_object = Mailing.objects.get(id=pk)
    mailing_object.status = 'C'
    mailing_object.save()
    return HttpResponseRedirect(reverse('mailings:mails'))
