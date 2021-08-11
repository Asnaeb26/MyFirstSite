from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from Homepage.models import *
import json
import random
import pickle
from pymemcache import Client as CacheClient
import datetime
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
    client = user_data(request)
    context = {'photo': client}
    return render(request, 'Homepage/index.html', context=context)


def set_day(request):
    day = int(request.POST['set_day'])
    Client.objects.filter(user_id=request.user.id).update(set_day=day)
    return HttpResponseRedirect('user_account')


def date(request):
    DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    client = Client.objects.filter(user_id=request.user.id)[0]
    current_year = datetime.date.today().year
    current_month = datetime.date.today().month
    # current_month = sliding_month(request)
    if client.set_day > DAYS_IN_MONTH[current_month]:
        client_set_day = DAYS_IN_MONTH[current_month]
    else:
        client_set_day = client.set_day
    first_day = datetime.date(current_year, current_month, client_set_day)
    last_day = first_day + datetime.timedelta(days=DAYS_IN_MONTH[(current_month + 1)])
    return first_day, last_day, current_month


def sort_date(request):
    first_day, last_day, current_month = date(request)
    # return HttpResponse(f'Тут будет показываться месяц под номером {last_day}')


def sliding_month(request):
    direction = request.GET.get('direction')
    if direction == 'next':
        current_month = datetime.date.today().month + 1
    elif direction == 'back':
        current_month = datetime.date.today().month - 1
    else:
        current_month = datetime.date.today().month
    # return current_month
    return HttpResponse(f'Тут будет показываться месяц под номером {current_month}')


def homepage(request):
    dollar, abbr = exchange_rates(request)
    first_day, last_day, current_month = date(request)
    client = user_data(request)
    hello, name = greeting(request)
    context = {'hello': hello,
               'name': name,
               'photo': client,
               'first_day': first_day,
               'last_day': last_day,
               }
    if request.GET.get('what') == 'show_income':
        # доходы
        all_income = Income.objects.filter(user=request.user, time_input__gte=first_day)
        total = 0
        sources = []
        for j in all_income:
            sources.append(j.source)
            total += j.add_income
        total_usd = round((total/dollar), 2)
        sources = set(sources)
        context['income'] = True
        context['total'] = round(total, 2)
        context['total_usd'] = total_usd
        context['sources'] = sources
        context['graphic_url'] = 'pie_fn_income'
    else:
        # расходы
        total = 0
        categories = []
        for i in SpentMoney.objects.filter(user=request.user, time_input__gte=first_day):
            categories.append(i.category)
            total += i.add_money
        total_usd = round((total/dollar), 2)
        categories = set(categories)
        context['categories'] = categories
        context['total'] = round(total, 2)
        context['total_usd'] = total_usd
        context['graphic_url'] = 'pie_fn'
    return render(request, 'Homepage/homepage.html', context)


def pie_fn(request):
    first_day, last_day, current_month = date(request)
    user_id = request.user.id
    current_costs = SpentMoney.objects.filter(user_id=user_id, time_input__gte=first_day)
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


def pie_fn_income(request):
    first_day, last_day, current_month = date(request)
    user_id = request.user.id
    current_costs = Income.objects.filter(user_id=user_id, time_input__gte=first_day)
    sources = []
    TOTAL = 0
    COSTS = []
    for i in current_costs:
        sources.append(i.source)
    sources = list(set(sources))
    for source in sources:
        total_for_source = 0
        for j in current_costs.filter(source=source):
            total_for_source += j.add_income
        TOTAL += total_for_source
        source_data = {'y': float(total_for_source), 'label': source}
        COSTS.append(source_data)
    for token in COSTS:
        percentage = (token['y'] * 100) / TOTAL
        token['y'] = round(percentage, 1)

    return JsonResponse(COSTS, safe=False)


def greeting(request):
    user = User.objects.filter(username=request.user)[0]
    name = user.first_name
    if name == '':
        name = request.user
    now = str(datetime.datetime.now())
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
    return hello, name


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
    return HttpResponseRedirect('homepage')


def add_income(request):
    if request.POST['new_source'] == '':
        source = request.POST['source']
    else:
        source = request.POST['new_source']
    Income(
        add_income=request.POST['add_income'],
        source=source,
        comment=request.POST['comment'],
        user_id=request.user.id
    ).save()
    return HttpResponseRedirect('homepage')


def edit_spending(request):
    current_id = request.POST['id']
    new_spending = float(request.POST['new_spending'])
    SpentMoney.objects.filter(id=current_id).update(add_money=new_spending)
    # current_id = int(request.POST['id'])
    # a = SpentMoney.objects.filter(id=current_id)
    # return HttpResponse(id)
    return HttpResponseRedirect('history')


def history(request):
    first_day, last_day, set_month = date(request)
    client = user_data(request)
    context = {
        'photo': client
    }
    if request.GET.get('what') == 'show_income':
        current_costs = Income.objects.filter(user_id=request.user.id, time_input__gte=first_day)
        total_for_category = 0
        ls = []
        for i in current_costs:
            ls.append(i.source)
            total_for_category += i.add_income
            total_for_category = round(float(total_for_category), 2)
        sources = set(ls)
        context['sources'] = sources
        context['total_for_category'] = total_for_category
        context['products'] = current_costs
        context['income'] = True
        if request.GET.get('id'):
            context['edit_id'] = int(request.GET.get('id'))
    else:
        current_costs = SpentMoney.objects.filter(user_id=request.user.id, time_input__gte=first_day)
        total_for_category = 0
        ls = []
        for i in current_costs:
            ls.append(i.category)
            total_for_category += i.add_money
            total_for_category = round(float(total_for_category), 2)
        categories = set(ls)
        context['categories'] = categories
        context['total_for_category'] = total_for_category
        context['products'] = current_costs
        if request.GET.get('id'):
            context['edit_id'] = int(request.GET.get('id'))
    return render(request, 'Homepage/history.html', context)


def sort_of(request):
    first_day, last_day, set_month = date(request)
    client = user_data(request)
    current_user = SpentMoney.objects.filter(user_id=request.user.id, time_input__gte=first_day)
    ls = []
    for i in current_user:
        ls.append(i.category)
    categories = set(ls)
    selected_category = current_user.filter(category=request.GET['category'])
    total_for_category = 0
    for cost in selected_category:
        total_for_category += cost.add_money
        total_for_category = round(float(total_for_category), 2)
    context = {
        'sort_categories': selected_category,
        'categories': categories,
        'photo': client,
        'total_for_category': total_for_category
    }

    return render(request, 'Homepage/history.html', context)


def sort_of_income(request):
    first_day, last_day, set_month = date(request)
    client = user_data(request)
    current_user = Income.objects.filter(user_id=request.user.id, time_input__gte=first_day)
    ls = []
    for i in current_user:
        ls.append(i.source)
    sources = set(ls)
    selected_source = current_user.filter(source=request.GET['source'])
    total_for_category = 0
    for cost in selected_source:
        total_for_category += cost.add_income
    context = {
        'sort_sources': selected_source,
        'sources': sources,
        'photo': client,
        'income': True,
        'total_for_category': total_for_category
    }
    return render(request, 'Homepage/history.html', context)


def del_spending(request):
    SpentMoney.objects.filter(id=request.GET['id']).delete()
    return HttpResponseRedirect('history')


def del_income(request):
    Income.objects.filter(id=request.GET['id']).delete()
    return HttpResponseRedirect('history?what=show_income')


def exchange_rates(request):
    response = requests.get('https://www.nbrb.by/api/exrates/rates/431')
    data = json.loads(response.text)
    dollar = data['Cur_OfficialRate']
    abbr = data['Cur_Abbreviation']
    return dollar, abbr


def planning(request):
    client = user_data(request)
    dollar, abbr = exchange_rates(request)
    context = {
        'dollar': dollar,
        'abbr': abbr,
        'photo': client
    }
    return render(request, 'Homepage/planning.html', context)


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
    if request.POST['password'] == request.POST['confirm_password']:
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
        return HttpResponseRedirect('homepage')
    else:
        context = {'error': True}
        return render(request, 'Homepage/registration.html', context)


def login_user(request):
    user = authenticate(
        username=request.POST['username'],
        password=request.POST['password']
    )
    if user is None:
        return render(request, 'Homepage/Log_in.html', {'error': True})
    else:
        login(request, user)
        return HttpResponseRedirect('homepage')


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
    context = {
        'User_info': request.user,
        'photo': client,
        'id': user_id}
    if request.GET.get('last_name') == 'edit':
        context['last_name_edit'] = True
    elif request.GET.get('first_name') == 'edik':
        context['first_name_edit'] = True
    return render(request, 'Homepage/user_account.html', context=context)


def edit_account(request):
    if request.GET.get('last_name') == 'new':
        User.objects.filter(username=request.user).update(last_name=request.POST['new_last_name'])
    else:
        User.objects.filter(username=request.user).update(first_name=request.POST['new_first_name'])
    return HttpResponseRedirect('user_account')
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
