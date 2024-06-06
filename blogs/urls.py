from django.urls import path
from django.views.decorators.cache import cache_page

from blogs.apps import BlogConfig
from blogs.views import BlogListView, BlogDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('', cache_page(60)(BlogListView.as_view()), name='blogs'),
    path('<slug:slug>/', cache_page(60)(BlogDetailView.as_view()), name='blog_detail')
]
