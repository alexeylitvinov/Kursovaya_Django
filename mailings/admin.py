from django.contrib import admin

from mailings.models import Mail, Mailing, MailingAttempt


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user')
    prepopulated_fields = {'slug': ('subject',)}


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('mail', 'first_send_date', 'send_time', 'status')


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'last_attempt_date', 'status')
