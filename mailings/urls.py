from django.urls import path

from mailings.apps import MailingsConfig
from mailings.services import complete_mailing, change_mailing_status
from mailings.views import MailListView, MailDetailView, MailUpdateView, MailDeleteView, MailCreateView, \
    MailingCreateView, MailingDetailView, MailingDeleteView, MailingUpdateView, MailingAttemptListView, MailingListView

app_name = MailingsConfig.name

urlpatterns = [
    path('', MailListView.as_view(), name='mails'),
    path('create/', MailCreateView.as_view(), name='mail_create'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('<slug:slug>/', MailDetailView.as_view(), name='mail_detail'),
    path('<slug:slug>/update/', MailUpdateView.as_view(), name='mail_update'),
    path('<slug:slug>/delete/', MailDeleteView.as_view(), name='mail_delete'),
    path('<slug:mail_slug>/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_attempts/<int:pk>/', MailingAttemptListView.as_view(), name='mailing_attempts'),
    path('schedule_mailing_tasks/<int:pk>/', change_mailing_status, name='schedule_mailing_tasks'),
    path('complete_mailing/<int:pk>/', complete_mailing, name='complete_mailing')
]
