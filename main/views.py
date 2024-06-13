from django.core.cache import cache
from django.shortcuts import render

from blogs.models import Blog
from mailings.models import Mailing
from users.models import Client


def index(request):
    """Отображение главной страницы"""
    unique_client_count = Client.objects.values('email').distinct().count()
    mailing_count = Mailing.objects.all().count()
    active_mailing_count = Mailing.objects.filter(status='R').count()
    latest_objects = cache.get('latest_objects')
    if not latest_objects:
        latest_objects = Blog.objects.order_by('-id')[:3]
        cache.set('latest_objects', latest_objects, 60 * 15)
    context = {
        'title': 'Главная',
        'unique_client_count': unique_client_count,
        'latest_objects': latest_objects,
        'mailing_count': mailing_count,
        'active_mailing_count': active_mailing_count
    }
    return render(request, 'main/index.html', context)


def about(request):
    """Отображение страницы О нас"""
    context = {
        'title': 'О нас',
        'phone': '+987654321123',
        'address': 'Россия, республика Татарстан, город Казань, улица Братьев Касимовых, дом 64'
    }
    return render(request, 'main/about.html', context)
