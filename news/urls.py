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
   path('authorlist/', AuthorList.as_view(), name='authors'),
   path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/', PostLists.as_view(), name='post_list'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('search/', SearchNews.as_view(), name='search_news'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('<int:pk>/edit/', ProfilUpdate.as_view(), name='user_edit'),
   path('add_subscribe/<int:pk>', add_subscribe, name='add_subscribe'),
   path('del_subscribe/<int:pk>', del_subscribe, name='del_subscribe'),
]