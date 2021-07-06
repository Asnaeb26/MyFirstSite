from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage),
    path('history', views.history),
    path('exchange_rates', views.exchange_rates),
    path('task2', views.task2),
    path('login_user', views.login_user),
    path('login', views.login2),
    path('logout', views.do_logout),
    path('registration', views.do_registration),
    path('register', views.register),
    path('ajax_path', views.ajax_path),
    path('uniq_user', views.uniq_user),
    path('user_account', views.user_account),
    path('add_money', views.add_money),

    # path('experiment', views.experiment)
]
