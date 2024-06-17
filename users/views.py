from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from config.settings import EMAIL_HOST_USER

from users.services import send_confirmation_email
from users.forms import UserRegisterForm, UserAuthenticationForm, ClientForm, UserForm, UserManagerForm
from users.models import User, Client


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Регистрация'}

    def form_valid(self, form):
        user = form.save()
        send_confirmation_email(self.request, user, EMAIL_HOST_USER)
        return super().form_valid(form)


class UserLoginView(LoginView):
    model = User
    form_class = UserAuthenticationForm
    success_url = reverse_lazy('users:login')
    template_name = "users/login.html"
    extra_context = {'title': 'Авторизация'}


class UserListView(ListView):
    model = User
    extra_context = {'title': 'Пользователи'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_count'] = User.objects.count() - 2
        return context

    def get_queryset(self):
        return User.objects.filter(is_superuser=False).exclude(groups__name='manager')


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:users')
    extra_context = {'title': 'Редактировать пользователя'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.request.user.pk
        return context

    def get_form_class(self):
        user = self.request.user
        if not user.groups.filter(name='manager').exists():
            return UserForm
        else:
            return UserManagerForm


class ClientListView(ListView):
    model = Client
    extra_context = {'title': 'Клиенты'}

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Client.objects.filter(user=self.request.user)
        else:
            return Client.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_count'] = self.get_queryset().count()
        return context


class ClientDetailView(DetailView):
    model = Client
    extra_context = {'title': 'Клиент'}


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('users:clients')
    extra_context = {'title': 'Добавить клиента'}

    def form_valid(self, form):
        client = form.save(commit=False)
        client.user = self.request.user
        try:
            client.save()
        except IntegrityError:
            messages.error(self.request, 'Клиент с таким email уже существует.')
            return super().form_invalid(form)
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('users:clients')
    extra_context = {'title': 'Редактировать клиента'}


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('users:clients')
    extra_context = {'title': 'Удалить клиента'}
