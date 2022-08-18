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
    paginate_by = 3
    #queryset = Author.objects.all()

    # def get_queryset(self):
    #     self.authorUser = get_object_or_404(Author, name=self.args[0])
    #     return Author.objects.filter(authorUser=self.authorUser)




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
    template_name = 'news/news_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        # post.postCategory = 'NW'
        # post.dateCreation = datetime.utcnow()
        # post.author = Author.objects.get(author_user=self.request.user)
        return super().form_valid(form)


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