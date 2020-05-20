from django.conf.urls import url
from . import views

#TEMPLATE URLS!
app_name = 'login_user'

urlpatterns = [
    url(r'^register/$', views.register, name='register')
]

