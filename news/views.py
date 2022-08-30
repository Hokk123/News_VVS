# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import *

class AuthorList(ListView):
    model = Author
    context_object_name = 'Authors'
    template_name = 'news/authors.html'
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
    #queryset = Post.objects.all()


class Post(DetailView):
    model = Post
    context_object_name = 'Post'
    template_name = 'news/post_detail.html'

