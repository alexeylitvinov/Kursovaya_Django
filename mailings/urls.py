from django.urls import path

from mailings.apps import MailingsConfig
from mailings.services import complete_mailing
from mailings.views import MailListView, MailDetailView, MailUpdateView, MailDeleteView, MailCreateView, \
    send_email_to_all_clients_view, MailingCreateView, MailingDetailView, MailingDeleteView, MailingUpdateView

app_name = MailingsConfig.name

urlpatterns = [
    path('', MailListView.as_view(), name='mails'),
    path('create/', MailCreateView.as_view(), name='mail_create'),
    path('<slug:slug>/', MailDetailView.as_view(), name='mail_detail'),
    path('<slug:slug>/update/', MailUpdateView.as_view(), name='mail_update'),
    path('<slug:slug>/delete/', MailDeleteView.as_view(), name='mail_delete'),
    path('<slug:mail_slug>/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('send-email/<slug:mail_slug>/', send_email_to_all_clients_view, name='send_email'),
    path('complete_mailing/<int:pk>/', complete_mailing, name='complete_mailing')
]
