from django.urls import path
# Импортируем созданное нами представление
from .views import *


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('authorlist/', AuthorList.as_view()),
   path('news/<int:pk>', Post.as_view()),
   path('news/', PostLists.as_view()),
]