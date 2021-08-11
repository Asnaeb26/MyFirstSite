from django.urls import path
from . import views


urlpatterns = [
    path('', views.login2),
    path('homepage', views.homepage),
    path('history', views.history),
    path('index', views.index),
    path('planning', views.planning),
    path('task2', views.task2),
    path('login_user', views.login_user),
    path('login', views.login2),
    path('logout', views.do_logout),
    path('registration', views.do_registration),
    path('register', views.register),
    path('ajax_path', views.ajax_path),
    path('uniq_user', views.uniq_user),
    path('user_account', views.user_account),
    path('edit_account', views.edit_account),
    path('add_money', views.add_money),
    path('add_income', views.add_income),
    path('get_user', views.server),
    path('del_spending', views.del_spending),
    path('del_income', views.del_income),
    path('sort_of', views.sort_of),
    path('sort_of_income', views.sort_of_income),
    path('sliding_month', views.sliding_month),
    path('edit_spending', views.edit_spending),
    path('pie_fn', views.pie_fn),
    path('pie_fn_income', views.pie_fn_income),
    path('test_fn', views.test_fn),
    path('date', views.date),
    path('set_day', views.set_day),
    path('sort_date', views.sort_date),
    # path('experiment', views.experiment)
]
