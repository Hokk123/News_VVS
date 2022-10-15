from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import m2m_changed, post_delete
from django.core.mail import mail_managers, send_mail
from .models import Post, Category
from .tasks import notify_subscribers_for_new_post



# создаём функцию обработчик с параметрами под регистрацию сигнала
@receiver(post_save, sender=Post)
def notify_post(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.title}! Опубликована новая запись.'
    else:
        subject = f'{instance.title} - статья была изменена.'

    mail_managers(
        subject=subject,
        message=instance.text,
    )


@receiver(post_delete, sender=Category)
def clear_cache_navbar(sender, instance, **kwargs):
    key = make_template_fragment_key('navbar')
    cache.delete(key)


@receiver(post_delete, sender=Post)
def clear_cache_navbar(sender, instance, **kwargs):
    cache.delete(f'post-id-{instance.pk}')
