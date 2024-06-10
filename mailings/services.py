from django.core.mail import send_mass_mail, BadHeaderError, send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from smtplib import SMTPException

# import mailings
# from apscheduler.schedulers.background import BackgroundScheduler
from config.settings import EMAIL_HOST_USER
from mailings.models import Mail, Mailing, MailingAttempt
from users.models import Client


def send_email_to_all_clients(request, mail_slug):
    # try:
    mail_object = Mail.objects.get(slug=mail_slug)
    mailing_object = Mailing.objects.get(mail_id=mail_object.id)
    clients = Client.objects.filter(user=request.user)

    # Обновляем статус рассылки
    mailing_object.status = 'R'
    mailing_object.save()

    for client in clients:
        try:
            # Отправляем письмо каждому клиенту индивидуально
            send_mail(
                subject=mail_object.subject,
                message=mail_object.body,
                from_email=EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False
            )
            # Создаем объект попытки рассылки с успешным статусом
            MailingAttempt.objects.create(
                mailing=mailing_object,
                client=client,
                last_attempt_date=timezone.now(),
                status=MailingAttempt.AttemptStatusChoices.SUCCESS,
                server_response='Письмо успешно отправлено'
            )
        except SMTPException as e:
            # Создаем объект попытки рассылки с неудачным статусом и ответом сервера
            MailingAttempt.objects.create(
                mailing=mailing_object,
                client=client,
                last_attempt_date=timezone.now(),
                status=MailingAttempt.AttemptStatusChoices.FAILURE,
                server_response=str(e)
            )
# except BadHeaderError as e:
#     # Обработка ошибки некорректного заголовка письма
#     raise e


# def send_email_to_all_clients(request, mail_slug):
#     try:
#         mail_object = Mail.objects.get(slug=mail_slug)
#         mail_id = mail_object.id
#         mailing_object = Mailing.objects.get(mail_id=mail_object.id)
#         mailing_id = mailing_object.id
#         clients = Client.objects.filter(user=request.user)
#         client_emails = [client.email for client in clients if client.email]
#         messages = [
#             (
#                 mail_object.subject,
#                 mail_object.body,
#                 EMAIL_HOST_USER,
#                 [email]
#             )
#             for email in client_emails
#         ]
#         num_sent = send_mass_mail(tuple(messages), fail_silently=False)
#         mailing = Mailing.objects.filter(mail_id=mail_id)
#         mailing.update(status='R')
#         for client in clients:
#             MailingAttempt.objects.create(
#                 mailing_id=mailing_id,
#                 client=client,
#                 last_attempt_date=timezone.now(),
#                 status=MailingAttempt.AttemptStatusChoices.SUCCESS
#                 if client.email in client_emails else MailingAttempt.AttemptStatusChoices.FAILURE,
#                 server_response=''  # Здесь может быть добавлен ответ сервера, если он доступен
#             )
#         return num_sent
#     except (BadHeaderError, SMTPException) as e:
#         mail_object = Mail.objects.get(slug=mail_slug)
#         mailing_object = Mailing.objects.get(mail_id=mail_object.id)
#         mailing_id = mailing_object.id
#         clients = Client.objects.filter(user=request.user)
#         for client in clients:
#             MailingAttempt.objects.create(
#                 mailing_id=mailing_id,
#                 client=client,
#                 last_attempt_date=timezone.now(),
#                 status=MailingAttempt.AttemptStatusChoices.FAILURE,
#                 server_response=str(e)  # Запись исключения как ответа сервера
#             )
#         raise e

# def send_email_to_all_clients(mailing):
#     # try:
#     clients = Client.objects.filter(user=mailing.mail.user)
#     for client in clients:
#         try:
#             # Отправляем письмо каждому клиенту индивидуально
#             send_mail(
#                 subject=mailing.mail.subject,
#                 message=mailing.mail.body,
#                 from_email=EMAIL_HOST_USER,
#                 recipient_list=[client.email],
#                 fail_silently=False
#             )
#             # Создаем объект попытки рассылки с успешным статусом
#             MailingAttempt.objects.create(
#                 mailing=mailing,
#                 client=client,
#                 last_attempt_date=timezone.now(),
#                 status=MailingAttempt.AttemptStatusChoices.SUCCESS,
#                 server_response='Письмо успешно отправлено'
#             )
#         except SMTPException as e:
#             # Создаем объект попытки рассылки с неудачным статусом и ответом сервера
#             MailingAttempt.objects.create(
#                 mailing=mailing,
#                 client=client,
#                 last_attempt_date=timezone.now(),
#                 status=MailingAttempt.AttemptStatusChoices.FAILURE,
#                 server_response=str(e)
#             )


def complete_mailing(request, pk):
    mailing_object = Mailing.objects.get(id=pk)
    mailing_object.status = 'CR'
    mailing_object.save()
    return HttpResponseRedirect(reverse('mailings:mails'))


# def schedule_mailing_tasks():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(check_and_send_mailings, 'interval', minutes=1)  # Проверка каждую минуту
#     scheduler.start()
#
#
# def check_and_send_mailings():
#     # Получаем текущее время
#     current_time = timezone.now()
#
#     # Находим все активные рассылки, которые нужно отправить
#     mailings_to_send = Mailing.objects.filter(
#         first_send_date__lte=current_time.date(),
#         send_time__lte=current_time.time(),
#         status=Mailing.StatusChoices.CREATED
#     )
#
#     for mailing in mailings_to_send:
#         # Проверяем, соответствует ли текущее время частоте рассылки и времени отправки
#         if should_send_now(mailing, current_time):
#             send_email_to_all_clients(mailing)
#
#
# def should_send_now(mailing, current_time):
#     # Получаем день недели и день месяца для текущего времени
#     day_of_week = current_time.weekday()
#     day_of_month = current_time.day
#
#     # Проверяем, совпадает ли текущее время с временем отправки
#     if current_time.time() < mailing.send_time:
#         # Если текущее время раньше времени отправки, не отправляем письмо
#         return False
#
#     # Проверяем частоту рассылки и определяем, нужно ли отправлять письмо
#     if mailing.frequency == Mailing.FrequencyChoices.DAILY:
#         # Для ежедневной рассылки отправляем каждый день
#         return True
#     elif mailing.frequency == Mailing.FrequencyChoices.WEEKLY:
#         # Для еженедельной рассылки проверяем, является ли сегодня тем днем недели, когда была отправлена первая рассылка
#         first_send_day_of_week = mailing.first_send_date.weekday()
#         return day_of_week == first_send_day_of_week
#     elif mailing.frequency == Mailing.FrequencyChoices.MONTHLY:
#         # Для ежемесячной рассылки проверяем, совпадает ли сегодняшний день месяца с днем первой отправки
#         first_send_day_of_month = mailing.first_send_date.day
#         return day_of_month == first_send_day_of_month
#
#     # Если частота не определена, не отправляем письмо
#     return False
