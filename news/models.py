from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import gettext_lazy as _



class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Имя'),)
    ratingAuthor = models.SmallIntegerField(default=0, verbose_name=_('Рейтинг'),)

    def __str__(self):
        return f'{self.authorUser}'

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_('Имя категории'),)
    subscribers = models.ManyToManyField(
        User, blank=True, through='CategorySubscribers', through_fields=('category', 'subscriber'),
    )

    def __str__(self):
        return self.name


class CategorySubscribers(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)    #verbose_name=_('Автор'),)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE, verbose_name=_('Тип контента'),)

    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'),)
    postCategory = models.ManyToManyField(Category, through='PostCategory', through_fields=('post', 'cat'))
    title = models.CharField(max_length=128, verbose_name=_('Название'),)
    text = models.TextField(verbose_name=_('Контент'),)
    rating = models.SmallIntegerField(default=0, verbose_name=_('Рейтинг'),)


    def __str__(self):
        return f'{self.text}\n' \
               f'Рейтинг статьи: {self.rating}\n' \
               f'Автор: {self.author}'


    def like(self):
        self.rating += 1
        self.save()


    def dislike(self):
        self.rating -= 1
        self.save()


    def preview(self):
        return self.text[0:123] + '...'


    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


    def censor(self):
        text = self.text
        variants = ['mat', 'soft', 'CLOUD', 'клиентов', 'конце']  # непристойные выражения

        ln = len(variants)
        filtred_message = ''
        string = ''
        pattern = '*'  # чем заменять непристойные выражения
        for i in text:
            string += i
            string2 = string.lower()

            flag = 0
            for j in variants:
                if not string2 in j:
                    flag += 1
                if string2 == j:
                    filtred_message += pattern * len(string)
                    flag -= 1
                    string = ''

            if flag == ln:
                filtred_message += string
                string = ''

        if string2 != '' and string2 not in variants:
            filtred_message += string
        elif string2 != '':
            filtred_message += pattern * len(string)

        return filtred_message



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.post.title} | {self.cat.name}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Пост'),)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Автор'),)
    text = models.TextField(verbose_name=_('Текст комментария'),)
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата комментария'),)
    rating = models.SmallIntegerField(default=0, verbose_name=_('Рейтинг'),)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.text
