from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from .models import Author, Category, Post, PostCategory, Comment, CategorySubscribers



class AuthorAdmin(TranslationAdmin):
    model = Author



class CategoryAdmin(TranslationAdmin):
    model = Category



class PostAdmin(TranslationAdmin):
    model = Post



class PostCategoryAdmin(TranslationAdmin):
    model = PostCategory



class CommentAdmin(TranslationAdmin):
    model = Comment



class UserAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('subscriber', 'category')  # оставляем только имя и цену товара
    list_filter = ('subscriber', 'category')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('name', 'category__name')  # тут всё очень похоже на фильтры из запросов в базу
    # actions = [nullfy_quantity]  # добавляем действия в список


# Register your models here.

admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CategorySubscribers)