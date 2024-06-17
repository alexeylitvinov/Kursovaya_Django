from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from mailings.forms import MailForm, MailingForm, MailingManagerForm
from mailings.models import Mail, Mailing, MailingAttempt


class MailListView(ListView):
    model = Mail
    extra_context = {'title': 'Письма'}

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Mail.objects.filter(user=self.request.user)
        else:
            return Mail.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Письма'
        context['mail_count'] = self.get_queryset().count()
        return context


class MailDetailView(DetailView):
    model = Mail
    extra_context = {'title': 'Письмо'}


class MailCreateView(CreateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailings:mails')
    extra_context = {'title': 'Создать письмо'}

    def form_valid(self, form):
        message = form.save(commit=False)
        message.user = self.request.user
        try:
            message.save()
        except IntegrityError:
            messages.error(self.request, 'Письмо с такой темой уже существует.')
            return super().form_invalid(form)
        return super().form_valid(form)


class MailUpdateView(UpdateView):
    model = Mail
    form_class = MailForm
    extra_context = {'title': 'Редактировать письмо'}

    def get_success_url(self):
        return reverse('mailings:mail_detail', kwargs={'slug': self.object.slug})


class MailDeleteView(DeleteView):
    model = Mail
    success_url = reverse_lazy('mailings:mails')
    extra_context = {'title': 'Удалить письмо'}


class MailingListView(ListView):
    model = Mailing
    extra_context = {'title': 'Все рассылки'}

    def get_queryset(self):
        # if self.request.user.has_any_group('manager'):
        if self.request.user.groups.filter(name='manager').exists():
            return Mailing.objects.all()


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    extra_context = {'title': 'Создать рассылку'}

    def form_valid(self, form):
        """Установления связи между объектами Mailing и Mail"""
        mail_slug = self.kwargs.get('mail_slug')
        form.instance.mail = Mail.objects.get(slug=mail_slug)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailings:mailing_detail', kwargs={'pk': self.object.pk})


class MailingDetailView(DetailView):
    model = Mailing
    extra_context = {'title': 'Рассылка'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
    extra_context = {'title': 'Удалить рассылку'}


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    extra_context = {'title': 'Редактировать рассылку'}

    def get_success_url(self):
        if self.request.user.groups.filter(name='manager').exists():
            return reverse('mailings:mailing_list')
        else:
            return reverse('mailings:mailing_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.request.user.pk
        return context

    def get_form_class(self):
        user = self.request.user
        if not user.groups.filter(name='manager').exists():
            return MailingForm
        else:
            return MailingManagerForm


class MailingAttemptListView(ListView):
    model = MailingAttempt
    extra_context = {'title': 'Логи рассылки'}

    def get_queryset(self):
        mailing_pk = self.kwargs.get('pk')
        return MailingAttempt.objects.filter(mailing__pk=mailing_pk).order_by('-last_attempt_date')
