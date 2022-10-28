from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from .models import *


class CategoryAdmin(TranslationAdmin):
    model = Category
    list_display = ['name']


class PostAdmin(TranslationAdmin):
    model = Post
    list_display = ('author', 'dateCreation')


class UserAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('subscriber', 'category')  # оставляем только имя и цену товара
    list_filter = ('subscriber', 'category')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('name', 'category__name')  # тут всё очень похоже на фильтры из запросов в базу
    # actions = [nullfy_quantity]  # добавляем действия в список


# Register your models here.

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(CategorySubscribers, UserAdmin)