from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from Homepage.models import *
import random
import pickle
from pymemcache import Client
from datetime import datetime
from django.utils.translation import ugettext as _, activate
import matplotlib.pyplot as plt
import numpy as np
import time
import datetime as dt
import requests


def main(request):
    activate(random.choice(['en', 'by']))
    return render(
        'Homepage/homepage.html', {'Hello': _('Привет мир')}
    )


def index(request):
    context = {'image': User.objects.filter(id=1)[0]}
    return render(request, "Homepage/homepage.html", context)


def homepage(request):
    ls = []
    for i in SpentMoney.objects.all():
        ls.append(i.category)
    categories = set(ls)
    hello = greeting()
    context = {'categories': categories, 'hello': hello}
    return render(request, 'Homepage/homepage.html', context)


def greeting():
    now = str(datetime.now())
    time_now = now.split(' ')[1]
    current_hour = int(time_now.split(':')[0])
    if 6 <= current_hour <= 11:
        hello = 'Доброе утро'
    elif 12 < current_hour < 18:
        hello = 'Добрый день'
    elif 18 <= current_hour < 23:
        hello = 'Добрый вечер'
    else:
        hello = 'Доброй ночи'
    return hello


def pie(request):
    all_objects = SpentMoney.objects.all()
    categories = []
    for label in all_objects:
        categories.append(label.category)
    categories = set(categories)
    labels = []
    values = []
    for j in categories:
        total = 0
        for i in all_objects:
            if i.category == j:
                total += i.add_money
        labels.append(j)
        values.append(total)
    # labels = ['Nokia', 'Samsung', 'Apple', 'Lumia']
    # values = [20, 50, 25, 5]

    # colors = ['yellow', 'green', 'red', 'blue']
    fig1, ax1 = plt.subplots()
    plt.pie(values, labels=labels, autopct='%1.2f%%')
    plt.axis('equal')
    plt.legend(loc='best')
    plt.savefig('Homepage/static/Homepage/pie.svg')
    return


def add_money(request):
    SpentMoney(
        add_money=request.POST['add_money'],
        comments=request.POST['comments'],
        category=request.POST['category']
    ).save()
    pie(request)  # Тут я вызываю pie, чтобы сохранить ихображение
    return HttpResponseRedirect('/')


def history(request):
    total = 0
    ls = []
    for i in SpentMoney.objects.all():
        ls.append(i.category)
        total += i.add_money
    categories = set(ls)
    context = {'products': SpentMoney.objects.all(), 'total': total, 'categories':categories}
    return render(request, 'Homepage/history.html', context)


def sort_of(request):
    ls = []
    for i in SpentMoney.objects.all():
        ls.append(i.category)
    categories = set(ls)
    selected_category = SpentMoney.objects.filter(category=request.GET['category'])
    context = {'sort_categories': selected_category, 'categories': categories}

    return render(request, 'Homepage/history.html', context)
    # return HttpResponse(context)


def del_spending(request):
    SpentMoney.objects.filter(id=request.GET['id']).delete()
    pie(request)
    return HttpResponseRedirect('history')


def exchange_rates(request):
    return render(request, 'Homepage/exchange_rates.html')


def task2(request):
    return render(request, 'Homepage/user_account.html')


def error(request):
    return render(request, 'Homepage/error_login.html')


def login2(request):
    return render(request, 'Homepage/Log_in.html')


def do_registration(request):
    return render(request, 'Homepage/registration.html')


def register(request):
    user = User.objects.create_user(
        request.POST['username'],
        password=request.POST['password'],
        first_name=' ',
        last_name=' ',
        email='',
    )
    login(request, user)
    return HttpResponseRedirect('/')


def login_user(request):
    user = authenticate(
        username=request.POST['username'],
        password=request.POST['password']
    )
    if user is None:
        pass
        # return render(request, 'Homepage/error_login.html')
        # HttpResponse('Такого пользователя не существует')
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


def ajax_path(request):
    response = {
        'message': 'Здарова отец'
    }

    return JsonResponse(response)


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
    return render(request, 'Homepage/user_account.html')


def two_list(ls1, ls2):
    ls3 = []
    for i in ls1:
        if i in ls2:
            ls3.append(i)
    return ls3


def randomiser(request):
    names = ['ac', 'fa', 'ek', 'do', 'ga', 'tu']
    for i in range(4000):
        a = random.randint(1, 1000)
        b = random.randint(1, 1000)
        c = a + b
        name = random.choice(names) + random.choice(names)
        Randomiser(name=name, number=c).save()
    return HttpResponseRedirect('/')


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


def randomiser(request):
    client = Client(('localhost', 11211))
    people = client.get('people')
    if people is None:
        people = []
        for person in Randomiser.objects.all():
            people.append(person.name)
        client.set(
            'people',
            pickle.dumps(people),
            expire=60
        )
    else:
        people = pickle.loads(people)

    return render(request, 'Homepage/homepage.html',
        {
            'people': people
        }
    )


