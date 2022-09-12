from time import sleep

from django.contrib.auth.models import User
from django.core import mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .models import Post, CategorySubscribers, Category, PostCategory, Author

from celery import shared_task


@shared_task
def notify_subscribers_for_new_post(id, title, content):
    """Отправка письма подписчикам при добавлении нового поста в категорию"""

    site = Site.objects.get_current()
    link = f'http://{127.0.0.1}:8000/{id}/'

    # Формируем список рассылки
    mailing_list = list(
        PostCategory.objects.filter(
            post_id=id
        ).select_related('category').values_list(
            'cat__subscribers__username',
            'cat__subscribers__first_name',
            'cat__subscribers__email',
            'cat__name',
        )
    )

    # Если список рассылки не пустой - отправляем каждому подписчику
    # индивидуальное письмо, за одно подключение к SMTP
    if any([all([len(mailing_list) == 1, mailing_list[0][2]]),
            len(mailing_list) > 1]):
        counter_mails = 0
        connection = None
        try:
            connection = mail.get_connection()
            connection.open()
        except Exception as e:
            print(e)
        else:
            for user, first_name, email, category in mailing_list:
                if not first_name:
                    first_name = user

                html_content = render_to_string(
                    'email/added_post.html',
                    {
                        'name': first_name,
                        'category': category,
                        'title': title,
                        'content': content,
                        'post_id': id,
                        'link': link,
                    }
                )
                message = mail.EmailMultiAlternatives(
                    subject=f'{first_name}, '
                            f'новая статья в категории "{category}"',
                    from_email='DEFAULT_FROM_EMAIL',
                    to=['vladimir_vs@list.ru'],
                    connection=connection,
                )
                message.attach_alternative(html_content, 'text/html')
                message.send()
                counter_mails += 1
        finally:
            connection.close()
        return f'Sent {counter_mails} Emails'


@shared_task
def weekly_notify():
    """Еженедельная рассылка новостей"""
    # Формируем ссылку для письма
    site = Site.objects.get_current()
    link = f'http://{127.0.0.1}:8000/'

    # Получаем список категорий, в которых есть новые статьи
    last_week = timezone.now() - timedelta(days=7)
    cats = list(Post.objects.filter(
        dateCreation__gte=last_week,
    ).values_list('postCategory', flat=True).distinct())

    # Отправляем письма
    counter_mails = 0
    connection = None
    for cat in cats:
        try:
            connection = mail.get_connection()
            connection.open()
        except Exception as e:
            print(e)
        else:
            # Получаем список подписчиков на категорию
            subscribers = list(CategorySubscribers.objects.filter(
                category=cat,
            ).values_list('subscriber', flat=True))
            if subscribers:
                # Подготавливаем и отправляем письмо
                for subscriber in subscribers:
                    receiver = User.objects.get(pk=subscriber)
                    category = Category.objects.get(pk=cat)
                    title_list = list(Post.objects.filter(
                        postCategory=cat,
                        dateCreation__gte=last_week,
                    ).values_list('pk', 'name'))
                    if not receiver.first_name:
                        firstname = receiver.username
                    else:
                        firstname = receiver.first_name
                    html_content = render_to_string(
                        'email/weekly_notify.html',
                        {
                            'name': firstname,
                            'category': category.name,
                            'titles': title_list,
                            'link': link,
                        }
                    )
                    message = mail.EmailMultiAlternatives(
                        subject=f'{firstname}, '
                                f'недельный обзор статей в категории '
                                f'"{category.name}"',
                        from_email='DEFAULT_FROM_EMAIL',
                        to=['vladimir_vs@list.ru'],
                        connection=connection,
                    )
                    message.attach_alternative(html_content, 'text/html')
                    message.send()
                    counter_mails += 1
        finally:
            connection.close()
    return f'{counter_mails} Emails is sent'