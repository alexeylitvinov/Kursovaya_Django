from django.shortcuts import render

from blogs.models import Blog
from users.models import Client


def index(request):
    unique_client_count = Client.objects.values('email').distinct().count()
    latest_objects = Blog.objects.order_by('-id')[:3]
    context = {
        'title': 'Главная',
        'unique_client_count': unique_client_count,
        'latest_objects': latest_objects
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'О нас',
        'phone': '+987654321123',
        'address': 'Россия, республика Татарстан, город Казань, улица Братьев Касимовых, дом 64'
    }
    return render(request, 'main/about.html', context)
