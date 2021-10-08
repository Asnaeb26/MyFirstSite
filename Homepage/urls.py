from django.urls import path
from . import views


urlpatterns = [
    path('', views.login2),
    path('homepage', views.homepage),
    path('history', views.history),
    path('index', views.index),
    path('planning', views.planning),
    path('login_user', views.login_user),
    path('login', views.login2),
    path('logout', views.do_logout),
    path('registration', views.do_registration),
    path('register', views.register),
    path('uniq_user', views.uniq_user),
    path('user_account', views.user_account),
    path('edit_account', views.edit_account),
    path('add_money', views.add_money),
    path('del_spending', views.del_spending),
    path('edit_spending', views.edit_spending),
    path('pie_fn', views.pie_fn),
    path('date', views.date),
    path('set_day', views.set_day),
]
