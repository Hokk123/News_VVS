"""News_VVS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
   path('i18n/', include('django.conf.urls.i18n')),
   path('admin/', admin.site.urls),
   path('post/', include('django.contrib.flatpages.urls')),
   # Делаем так, чтобы все адреса из нашего приложения (news/urls.py)
   # подключались к главному приложению с префиксом products/.
   path('news/', include('news.urls')),
   path('', include('protect.urls')),
   path('sign/', include('sign.urls')),
   path('accounts/', include('allauth.urls')),
]


# urlpatterns += i18n_patterns(
#    path('', include('news.urls')),
# )