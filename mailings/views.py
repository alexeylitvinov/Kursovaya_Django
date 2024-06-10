from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from mailings.forms import MailForm, MailingForm
from mailings.models import Mail, Mailing, MailingAttempt
from mailings.services import send_email_to_all_clients


class MailListView(ListView):
    model = Mail

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Mail.objects.filter(user=self.request.user)
        else:
            return Mail.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письма'
        context['mail_count'] = self.get_queryset().count()
        return context


class MailDetailView(DetailView):
    model = Mail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо'
        return context


class MailCreateView(CreateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailings:mails')

    def form_valid(self, form):
        message = form.save(commit=False)
        message.user = self.request.user
        try:
            message.save()
        except IntegrityError:
            messages.error(self.request, 'Письмо с такой темой уже существует.')
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать письмо'
        return context


class MailUpdateView(UpdateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailings:mails')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать письмо'
        return context


class MailDeleteView(DeleteView):
    model = Mail
    success_url = reverse_lazy('mailings:mails')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить письмо'
        return context


def send_email_to_all_clients_view(request, mail_slug):
    send_email_to_all_clients(request, mail_slug)
    mails_url = reverse('mailings:mails')
    return HttpResponseRedirect(mails_url)


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = '/mailings/'

    def form_valid(self, form):
        mail_slug = self.kwargs.get('mail_slug')
        form.instance.mail = Mail.objects.get(slug=mail_slug)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать рассылку'
        return context


class MailingDetailView(DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Рассылка'
        context['mail_slug'] = self.object.mail.slug
        user = self.object.mail.user
        clients = user.client_set.all()
        for client in clients:
            try:
                client.last_mailing_attempt = MailingAttempt.objects.filter(
                    mailing=self.object,
                    client=client
                ).latest('last_attempt_date')
            except MailingAttempt.DoesNotExist:
                client.last_mailing_attempt = None
        context['clients'] = clients
        return context


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailings:mails')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить рассылку'
        return context


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mails')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать рассылку'
        return context
