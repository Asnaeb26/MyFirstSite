from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from Homepage.models import *
import random
import pickle
from pymemcache import Client as CacheClient
from datetime import datetime
from django.utils.translation import ugettext as _, activate
import matplotlib.pyplot as plt
import numpy as np
import time
import requests


def user_data(request):
    user_id = User.objects.filter(username=request.user)[0].id
    client = Client.objects.filter(user_id=user_id)[0]
    return client


def index(request):
    client = user_data()
    context = {'photo': client}
    return render(request, 'Homepage/index.html', context=context)


def homepage(request):
    client = user_data(request)
    ls = []
    for i in SpentMoney.objects.all():
        ls.append(i.category)
    categories = set(ls)
    hello = greeting()
    context = {'categories': categories, 'hello': hello, 'photo': client}
    return render(request, 'Homepage/homepage.html', context)


def greeting():
    now = str(datetime.now())
    time_now = now.split(' ')[1]
    current_hour = int(time_now.split(':')[0])
    if 6 <= current_hour <= 11:
        hello = 'Доброе утро'
    elif 12 <= current_hour < 18:
        hello = 'Добрый день'
    elif 18 <= current_hour < 23:
        hello = 'Добрый вечер'
    else:
        hello = 'Доброй ночи'
    return hello


def add_money(request):
    if request.POST['new_category'] == '':
        category = request.POST['category']
    else:
        category = request.POST['new_category']
    SpentMoney(
        add_money=request.POST['add_money'],
        category=category,
        comments=request.POST['comments'],
        user_id=request.user.id
    ).save()
    return HttpResponseRedirect('/')


def history(request):
    client = user_data(request)
    current_user = SpentMoney.objects.filter(user_id=request.user.id)
    total = 0
    ls = []
    for i in current_user:
        ls.append(i.category)
        total += i.add_money
    categories = set(ls)
    context = {
        'products': current_user,
        'total': total,
        'categories': categories,
        'photo': client

    }
    return render(request, 'Homepage/history.html', context)


def sort_of(request):
    current_user = SpentMoney.objects.filter(user_id=request.user.id)
    ls = []
    for i in current_user:
        ls.append(i.category)
    categories = set(ls)
    selected_category = current_user.filter(category=request.GET['category'])
    context = {'sort_categories': selected_category, 'categories': categories}

    return render(request, 'Homepage/history.html', context)
    # return HttpResponse(context)


def del_spending(request):
    SpentMoney.objects.filter(id=request.GET['id']).delete()
    return HttpResponseRedirect('history')


def exchange_rates(request):
    client = user_data(request)
    context = {
        'photo': client
    }
    return render(request, 'Homepage/exchange_rates.html', context)


def task2(request):
    return render(request, 'Homepage/user_account.html')


def error(request):
    return render(request, 'Homepage/error_login.html')


# ------block with user------------


def login2(request):
    return render(request, 'Homepage/Log_in.html')


def do_registration(request):
    return render(request, 'Homepage/registration.html')


def register(request):
    user = User.objects.create_user(
        request.POST['username'],
        password=request.POST['password'],
        email=request.POST['email'],
        first_name='',
        last_name='',
    )
    client = Client(user_id=user.id, avatar='cat.png')
    client.save()
    login(request, user)
    return HttpResponseRedirect('/')


def login_user(request):
    user = authenticate(
        username=request.POST['username'],
        password=request.POST['password']
    )
    if user is None:
        return render(request, 'Homepage/Log_in.html', {'error': True})
    else:
        login(request, user)
        return HttpResponseRedirect('/')


def do_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('login')
    else:
        return HttpResponse('Такой пользователь не залогинен')


def uniq_user(request):
    # try:
    if len(User.objects.filter(username=request.POST['a'])) == 0:
        exist = 'n'
    else:
        exist = 'y'
    response = {
        'message': exist
    }

    # except IntegrityError
    return JsonResponse(response)


def user_account(request):
    user_id = User.objects.filter(username=request.user)[0].id
    client = Client.objects.filter(user_id=user_id)[0]
    context = {'User_info': request.user, 'photo': client, 'id': user_id}
    return render(request, 'Homepage/user_account.html', context=context)


# ___________end block with user_____________


def ajax_path(request):
    response = {
        'message': 'Здарова отец ' + request.POST['a']
    }

    return JsonResponse(response)


def test_fn(request):
    mod = SpentMoney.objects.all()
    numb = int(request.POST['a']) - 9
    answer = {
        'b': numb,
        'c': request.POST['a']
    }
    return JsonResponse(answer)


def percent(total, num):
    percentage = (num * 100)/total
    return percentage


def pie_fn(request):
    user_id = request.user.id
    current_costs = SpentMoney.objects.filter(user_id=user_id)
    categories = []
    TOTAL = 0
    COSTS = []
    for i in current_costs:
        categories.append(i.category)
    categories = list(set(categories))
    for category in categories:
        total_for_category = 0
        for j in current_costs.filter(category=category):
            total_for_category += j.add_money
        TOTAL += total_for_category
        category_data = {'y': float(total_for_category), 'label': category}
        COSTS.append(category_data)
    for token in COSTS:
        percentage = (token['y'] * 100) / TOTAL
        token['y'] = round(percentage, 1)

    return JsonResponse(COSTS, safe=False)
    # return HttpResponse(categories)


def two_list(ls1, ls2):
    ls3 = []
    for i in ls1:
        if i in ls2:
            ls3.append(i)
    return ls3


def server(request):
    if 'id' in request.POST:
        Person3.objects.filter(
            id=request.POST['id']
        ).update(
            name=request.POST['name'],
            age=int(request.POST['age'])
        )
        return JsonResponse({'status': 'OK'})
    else:
        ls = []
        id_new = request.GET['id']
        Person3.objects.filter(id=id_new)
        for i in Person3.objects.filter(id=id_new):
            ls.append({'name': i.name, 'age': i.age})
        return JsonResponse({'people': ls})

# def dollars(request):
#     get_response()
#     return render(request, 'Homepage/exchange_rates.html')


# def experiment(request):
#     size = 300000
#     slice_size = 500
#     Person3.objects.all().delete()
#     for _ in range(int(size / slice_size)):
#         slice = []
#         for _ in range(slice_size):
#             slice.append(
#                 Person3(
#                     name=str(random.randint(1, 1000)),
#                     credit_card_number=str(
#                         random.randint(10**70, 10**80)
#                     )
#                 )
#             )
#         Person3.objects.bulk_create(slice, slice_size)
#
#     sum = 0
#     for _ in range(100):
#         start = datetime.now()
#         list(Person3.objects.filter(
#             credit_card_number=random.randint(
#                 10**70, 10**80
#             )
#         ))
#         delta = (datetime.now() - start).total_seconds()
#         sum = sum + delta
#     print("Время выполнения 100 запрсосов: " +
#           str(sum) + ' секунд')
#
#     return HttpResponse('Ok')
