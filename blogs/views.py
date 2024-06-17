from django.views.generic import ListView, DetailView

from blogs.models import Blog


class BlogListView(ListView):
    model = Blog
    context_object_name = 'all_objects'
    extra_context = {'title': 'Блоги'}


class BlogDetailView(DetailView):
    model = Blog
    extra_context = {'title': 'Блог'}

    def get_object(self, queryset=None):
        """
        Формирование счетчика просмотров
        """
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object
