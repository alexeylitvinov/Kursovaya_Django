from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from config.settings import EMAIL_HOST_USER

from users.services import send_confirmation_email
from users.forms import UserRegisterForm, UserAuthenticationForm, ClientForm
from users.models import User, Client


class UserCreateView(CreateView):
    """
    Регистрация нового пользователя
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        """
        Подтверждение регистрации с отсылкой письма на email пользователя
        """
        user = form.save()
        send_confirmation_email(self.request, user, EMAIL_HOST_USER)
        return super().form_valid(form)


class UserLoginView(LoginView):
    """
    Авторизация пользователя
    """
    model = User
    form_class = UserAuthenticationForm
    success_url = reverse_lazy('users:login')
    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context


class UserListView(ListView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        context['user_count'] = User.objects.count() - 1
        return context

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Client.objects.filter(user=self.request.user)
        else:
            return Client.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Клиенты'
        context['client_count'] = self.get_queryset().count()
        return context


class ClientDetailView(DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Клиент'
        return context


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('users:clients')

    def form_valid(self, form):
        client = form.save(commit=False)
        client.user = self.request.user
        try:
            client.save()
        except IntegrityError:
            messages.error(self.request, 'Клиент с таким email уже существует.')
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить клиента'
        return context


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('users:clients')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать клиента'
        return context


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('users:clients')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить клиента'
        return context
