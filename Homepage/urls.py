from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage),
    path('contacts', views.contact),
    path('about-us', views.about),
    path('task1', views.task1),
    path('task2', views.task2),
    path('login_user', views.login_user),
    path('login', views.login2),
    path('logout', views.do_logout),
    path('registration', views.do_registration),
    path('register', views.register),
    path('ajax_path', views.ajax_path),
    path('uniq_user', views.uniq_user)


]
