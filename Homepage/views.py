import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from Homepage.models import Client, Income, SpentMoney, User
from Homepage import logic


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


def homepage(request):
    dollar, abbr = logic.exchange_rates()
    # direction = request.GET.get('direction')
    first_day, last_day, current_month = logic.date(request)
    client = user_data(request)
    hello, name = logic.greeting(request)
    context = {'hello': hello,
               'name': name,
               'photo': client,
               'first_day': first_day,  # Год - месяц - день
               'last_day': last_day,
               'current_month': current_month,
               }
    if request.GET.get('action') == 'show_income':
        model = Income
        context['income'] = True
        context['graphic_url'] = 'pie_fn?action=show_income'
    else:
        model = SpentMoney
        context['graphic_url'] = 'pie_fn'
    if request.GET.get('action') == 'show_error':
        context['category_error'] = True
    total = 0
    categories = []
    for i in model.objects.filter(user=request.user,
                                  time_input__gte=first_day,
                                  time_input__lte=last_day):
        categories.append(i.category)
        total += i.add_money
    total_usd = round((total / dollar), 2)
    categories = set(categories)
    context['categories'] = categories
    context['total'] = round(total, 2)
    context['total_usd'] = total_usd
    return render(request, 'Homepage/homepage.html', context)


def pie_fn(request):
    if request.GET.get('action') == 'show_income':
        model = Income
    else:
        model = SpentMoney
    first_day = datetime.datetime.strptime(request.POST.get('start'), "%Y-%m-%d")
    last_day = datetime.datetime.strptime(request.POST.get('finish'), "%Y-%m-%d")
    current_costs = model.objects.filter(user_id=request.user.id, time_input__gte=first_day, time_input__lte=last_day)
    categories = []
    TOTAL = 0
    costs = []
    if len(current_costs) != 0:
        for i in current_costs:
            categories.append(i.category)
        categories = list(sorted(set(categories)))
        for category in categories:
            total_for_category = 0
            for j in current_costs.filter(category=category):
                total_for_category += j.add_money
            TOTAL += total_for_category
            category_data = {'y': float(total_for_category), 'label': category}
            costs.append(category_data)
        for token in costs:
            percentage = (token['y'] * 100) / TOTAL
            token['per'] = round(percentage, 1)
    else:
        costs = [{'y': 1, 'label': 'Пусто', 'p': 100}]
    return JsonResponse(costs, safe=False)


def add_money(request):
    if request.POST.get('type') == 'Income':
        model = Income
    else:
        model = SpentMoney
    try:
        if request.POST['new_category'] == '':
            category = request.POST['category']
        else:
            category = request.POST['new_category']
    except Exception:
        return HttpResponseRedirect('homepage?action=show_error')

    model(
        add_money=request.POST['add_money'],
        category=category,
        comments=request.POST['comments'],
        user_id=request.user.id
    ).save()
    if model == SpentMoney:
        return HttpResponseRedirect('homepage')
    else:
        return HttpResponseRedirect('homepage?action=show_income')


def edit_spending(request):
    current_id = request.POST['id']
    new_spending = float(request.POST['new_spending'])
    if request.GET.get('condition') == 'edit_income':
        Income.objects.filter(id=current_id).update(add_money=new_spending)
        return HttpResponseRedirect('history?action=show_income')
    else:
        SpentMoney.objects.filter(id=current_id).update(add_money=new_spending)
        return HttpResponseRedirect('history')


def history(request):
    first_day, last_day, set_month = logic.date(request)
    client = user_data(request)
    context = {
        'photo': client
    }
    if request.GET.get('action') == 'show_income':
        model = Income
        context['income'] = True
    else:
        model = SpentMoney
    current_costs = model.objects.filter(user_id=request.user.id, time_input__gte=first_day)
    categories = [item.category for item in current_costs]
    if request.GET.get('condition') == 'sorted':
        current_costs = current_costs.filter(category=request.GET['category'])
    total_for_category = 0
    for i in current_costs:
        total_for_category += i.add_money
    context['categories'] = sorted(set(categories))
    context['total_for_category'] = round(float(total_for_category), 2)
    context['products'] = current_costs
    if request.GET.get('id'):
        context['edit_id'] = int(request.GET.get('id'))
    return render(request, 'Homepage/history.html', context)


def del_spending(request):
    if request.GET.get('action') == 'del_income':
        Income.objects.filter(id=request.GET['id']).delete()
        return HttpResponseRedirect('history?action=show_income')
    else:
        SpentMoney.objects.filter(id=request.GET['id']).delete()
        return HttpResponseRedirect('history')


def planning(request):
    client = user_data(request)
    dollar, abbr = logic.exchange_rates()
    context = {
        'dollar': dollar,
        'abbr': abbr,
        'photo': client
    }
    return render(request, 'Homepage/planning.html', context)


# ------block with user------------


def login2(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('homepage')
        # return render(request, 'Homepage/homepage.html')
    else:
        return render(request, 'Homepage/Log_in.html')


def do_registration(request):
    return render(request, 'Homepage/registration.html')


def register(request):
    try:
        if User.objects.filter(email=request.POST['email']):
            context = {'uniq_error': True}
            return render(request, 'Homepage/registration.html', context)
        if request.POST['password'] == request.POST['confirm_password']:
            user = User.objects.create_user(
                request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email'],
                first_name='',
                last_name='')
            client = Client(user_id=user.id, avatar='cat.png')
            client.save()
            login(request, user)
            return HttpResponseRedirect('homepage')
        else:
            context = {'error': True}
            return render(request, 'Homepage/registration.html', context)
    except IntegrityError:
        context = {'uniq_error': True}
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
    if len(User.objects.filter(username=request.POST['a'])) == 0:
        exist = 'n'
    else:
        exist = 'y'
    response = {
        'message': exist
    }
    return JsonResponse(response)


def user_account(request):
    user_id = User.objects.filter(username=request.user)[0].id
    client = Client.objects.filter(user_id=user_id)[0]
    current_set_day = Client.objects.filter(user_id=request.user.id)[0].set_day
    context = {
        'User_info': request.user,
        'photo': client,
        'id': user_id,
        'set_day': current_set_day,
    }
    if request.GET.get('last_name') == 'edit':
        context['last_name_edit'] = True
    elif request.GET.get('first_name') == 'edit':
        context['first_name_edit'] = True
    elif request.GET.get('set_day') == 'edit':
        context['set_day_edit'] = True
    return render(request, 'Homepage/user_account.html', context=context)


def edit_account(request):
    if request.GET.get('last_name') == 'new':
        User.objects.filter(username=request.user).update(last_name=request.POST['new_last_name'])
    else:
        User.objects.filter(username=request.user).update(first_name=request.POST['new_first_name'])
    return HttpResponseRedirect('user_account')
# ___________end block with user_____________
