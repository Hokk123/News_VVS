# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.shortcuts import render, redirect, reverse
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from .filters import *
from .forms import *
from .models import Post, Author, Category, Comment
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создания объекта письма с html
from django.core.mail import mail_admins  # импортируем функцию для массовой отправки писем админам
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from django.conf import settings
from django.utils import timezone


# def notify_manager_models(sender, instance, created, **kwargs):
#     mail_managers(
#         subject=f'{instance.client_name} {instance.date.strftime("%d %m %Y")}',
#         message=instance.message,
#     )
#
# post_save.connect(notify_manager_models, sender=Post)


class AuthorList(LoginRequiredMixin, ListView):
    model = Author
    context_object_name = 'Authors'
    template_name = 'news/authors.html'
    # paginate_by = 100
    # queryset = Author.objects.all()

    # def get_queryset(self):
    #     self.authorUser = get_object_or_404(Author, name=self.args[0])
    #     return Author.objects.filter(authorUser=self.authorUser)


class PostLists(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
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
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    context_object_name = 'Post'
    template_name = 'news/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Подтягиваем комментарии к статье
        # context['comments'] = Comment.objects.select_related().filter(
        #     post_id=self.kwargs['pk']
        # )
        context['is_not_subscribe'] = not self.request.user.groups.filter(name='subscribers').exists()
        context['is_subscribe'] = self.request.user.groups.filter(name='subscribers').exists()
        return context

    def subscribe(request, pk):
        context = {
            'user': request.user,
            'cat': Category.objects.get(id=pk),
            'is_subscribed': Category.objects.get(id=pk).subscribers.filter(id=request.user.id).exists()
        }
        return render(request, 'news/subscribe.html', context)



#подписка
@login_required
def add_subscribe(request, **kwargs):
    user = request.user
    cat_number = int(kwargs['pk'])
    category = Category.objects.get(pk=cat_number)
    category.subscribers.add(user)
    return redirect('/news/')

#отписка
@login_required
def del_subscribe(request, **kwargs):
    user = request.user
    cat_number = int(kwargs['pk'])
    category = Category.objects.get(pk=cat_number)
    category.subscribers.remove(user)
    return redirect('/news/')


# Добавляем новое представление для создания новостей.
class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    permission_required = ('news.add_post', 'news.change_post', 'news.delete_post')
    template_name = 'news/news_create.html'
    success_url = reverse_lazy('post_list')
    # author = Author.objects.get(authorUser=self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Проверяем количество постов автора за текущие сутки
        limit = settings.DAILY_POST_LIMIT

        context['limit'] = limit
        last_day = timezone.now() - timedelta(days=1)

        posts_day_count = Post.objects.filter(
            author__authorUser=self.request.user,
            dateCreation__gte=last_day,
        ).count()
        context['count'] = posts_day_count
        context['post_limit'] = posts_day_count < limit
        return context

    def post(self, request, *args, **kwargs):
        post_mail = Post(
            text=request.POST['text'],
            title=request.POST['title'],
        )
        post_mail.save()
        html_content = render_to_string(
            'email/cat_subscribe.html',
            {
                'news': post_mail,
            }
        )
        load_dotenv()
        msg = EmailMultiAlternatives(
            subject=f'Новая публикация в вашем любимом разделе.',
            body=post_mail.title,
            from_email='DEFAULT_FROM_EMAIL',
            to=['vladimir_vs@list.ru'],
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем

        return redirect('/news/news/')


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


class ProfilUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = ProfilForm
    model = Author
    permission_required = (
        'news.change_author',
    )
    template_name = 'news/user_edit.html'
    success_url = reverse_lazy('authors')


# Добавляем представление для изменения.
class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostForm
    model = Post
    permission_required = (
        'news.change_post',
    )
    template_name = 'news/post_edit.html'
    success_url = reverse_lazy('post_list')


# Представление для удаления.
class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    permission_required = (
        'news.delete_post',
    )
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')


#  Подписка на категорию
# @login_required
# def add_subscribe(request, **kawargs):
#     cat_number = int(kwargs['pk'])
#     is_subscribed = category.subscribers.filter(id=user.id).exists()
#     if not is_subscribed:
#         # Добавляем подписчика в базу и
#         # отправляем письмо об успешной подписке
#         Category.objects.get(pk=cat_number).subscribers.add(request.user)
#         html_content = render_to_string(
#             'email/cat_subscribe.html',
#             {
#                 'user': user,
#                 'category': category.name,
#             }
#         )
#         message = EmailMultiAlternatives(
#             subject=f'{user}, подписка на новости {category.name} оформлена!',
#             from_email=settings.EMAIL,
#             to=[user.email],
#         )
#         message.attach_alternative(html_content, 'text/html')
#         try:
#             message.send()
#         except Exception as e:
#             print(e)
#         finally:
#             return redirect('/news/news/')

