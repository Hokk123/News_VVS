# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)

from .filters import *
from .forms import *
from .models import Post, Author


class AuthorList(ListView):
    model = Author
    context_object_name = 'Authors'
    template_name = 'news/authors.html'
    # paginate_by = 100
    #queryset = Author.objects.all()

    # def get_queryset(self):
    #     self.authorUser = get_object_or_404(Author, name=self.args[0])
    #     return Author.objects.filter(authorUser=self.authorUser)




class AuthorList(ListView):
    model = Author




class PostLists(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'title'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news/news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'News'
    paginate_by = 2

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context



class PostDetail(DetailView):
    model = Post
    context_object_name = 'Post'
    template_name = 'news/post_detail.html'



# Добавляем новое представление для создания новостей.
class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    permission_required = (
        'news.add_post',
    )
    template_name = 'news/news_create.html'
    success_url = reverse_lazy('post_list')

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.author = Author.objects.get(user=self.request.user)
    #     postauthor = self.object.author
    #     DAILY_POST_LIMIT = 30
    #     error_message = f'No more than {DAILY_POST_LIMIT} posts a day, dude!'
    #     posts = Post.objects.all()
    #
    #     today_posts_count = 0
    #     for post in posts:
    #         if post.author == postauthor:
    #             time_delta = datetime.now().date() - post.time_pub.date()
    #             if time_delta.total_seconds() < (60*60*24):
    #                 today_posts_count += 1
    #
    #     if today_posts_count < DAILY_POST_LIMIT:
    #         self.object.save()
    #         id_new_post = self.object.id
    #         # print(id_new_post)
    #         print('notifying subscribers from view (no signals)...', id_new_post)
    #         new_post_subscription.apply_async([id_new_post], countdown = 5)
    #
    #         # cat = Category.objects.get(pk=self.request.POST['cats'])
    #         # self.object.cats.add(cat)
    #
    #         validated = super().form_valid(form)
    #
    #     else:
    #         messages.error(self.request, self.error_message)
    #         validated = super().form_invalid(form)
    #
    #     return validated


class SearchNews(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'search'  # имя списка

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class ProfilUpdate(UpdateView):
    form_class = ProfilForm
    model = Author
    template_name = 'news/user_edit.html'
    success_url = reverse_lazy('post_list')



# Добавляем представление для изменения.
class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    success_url = reverse_lazy('post_list')


# Представление для удаления.
class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')