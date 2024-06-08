from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import MailListView, MailDetailView, MailUpdateView, MailDeleteView, MailCreateView, \
    send_email_to_all_clients_view

app_name = MailingsConfig.name

urlpatterns = [
    path('', MailListView.as_view(), name='mails'),
    path('create/', MailCreateView.as_view(), name='mail_create'),
    path('<slug:slug>/', MailDetailView.as_view(), name='mail_detail'),
    path('<slug:slug>/update/', MailUpdateView.as_view(), name='mail_update'),
    path('<slug:slug>/delete/', MailDeleteView.as_view(), name='mail_delete'),
    path('send-email/<slug:mail_slug>/', send_email_to_all_clients_view, name='send_email'),
]
