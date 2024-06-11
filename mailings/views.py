from django.contrib import messages
from django.db import IntegrityError
# from django.http import HttpResponseRedirect
# from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from mailings.forms import MailForm, MailingForm
from mailings.models import Mail, Mailing, MailingAttempt


# from mailings.services import send_email_to_all_clients, schedule_mailing_tasks


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

    # success_url = reverse_lazy('mailings:mails')
    def get_success_url(self):
        # self.object - это объект Mailing, который был обновлен
        return reverse('mailings:mail_detail', kwargs={'slug': self.object.slug})

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


# def send_email_to_all_clients_view(request, mail_slug):
#     send_email_to_all_clients(request, mail_slug)
#     mails_url = reverse('mailings:mails')
#     return HttpResponseRedirect(mails_url)

# def start_schedule(request):
#     # Запускаем задачу планировщика
#     schedule_mailing_tasks()
#
#     # Перенаправляем пользователя обратно на страницу с рассылками
#     return redirect(reverse('mailings:mails'))


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm

    # success_url = '/mailings/'

    def form_valid(self, form):
        """Установления связи между объектами Mailing и Mail"""
        mail_slug = self.kwargs.get('mail_slug')
        form.instance.mail = Mail.objects.get(slug=mail_slug)
        return super().form_valid(form)

    # def get_success_url(self):
    #     mail_slug = self.object.mail.slug
    #     # Используем slug созданного объекта для создания URL
    #     return reverse('mailings:mail_detail', kwargs={'slug': mail_slug})

    def get_success_url(self):
        # self.object - это объект Mailing, который был обновлен
        return reverse('mailings:mailing_detail', kwargs={'pk': self.object.pk})

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

    # success_url = reverse_lazy('mailings:mailing_detail')
    def get_success_url(self):
        # self.object - это объект Mailing, который был обновлен
        return reverse('mailings:mailing_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать рассылку'
        return context


class MailingAttemptListView(ListView):
    model = MailingAttempt

    def get_queryset(self):
        """
        Переопределите метод `get_queryset`, чтобы отфильтровать попытки рассылки
        для конкретного `mailing_id`.
        """
        mailing_pk = self.kwargs.get('pk')  # Получите `mailing_id` из URL-параметров
        return MailingAttempt.objects.filter(mailing__pk=mailing_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Логи рассылки'
        return context
