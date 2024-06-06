from django.views.generic import ListView, DetailView

from blogs.models import Blog


class BlogListView(ListView):
    model = Blog
    context_object_name = 'all_objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блоги'
        return context


class BlogDetailView(DetailView):
    """
    Детальный просмотр объекта Блог
    """
    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог'
        return context

    def get_object(self, queryset=None):
        """
        Формирование счетчика просмотров
        """
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object
