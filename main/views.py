from django.shortcuts import render


def index(request):
    context = {
        'title': 'Главная'
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'О нас',
        'phone': '+987654321123',
        'address': 'Россия, республика Татарстан, город Казань, улица Братьев Касимовых, дом 64'
    }
    return render(request, 'main/about.html', context)
