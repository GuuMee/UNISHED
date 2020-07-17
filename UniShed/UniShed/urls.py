"""UniShed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from login_user import views

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('user/', include('login_user.urls')),
    path('schedule/', include('schedule.urls')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('logout/', views.user_logout, name='logout'),
    path('special/', views.special, name='special'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.site.site_header = "UNISHED Администрирование"
admin.site.site_title = "UNISHED База Данных"
admin.site.index_title = "Система Базы Данных UNISHED"