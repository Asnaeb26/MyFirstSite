from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def index(request):
    return render(request, "Homepage/index.html")


def homepage(request):
    return render(request, "Homepage/homepage.html")


def about(request):
    return render(request, "Homepage/about-us.html")


def contact(request):
    return render(request, "Homepage/contacts.html")


def task1(request):
    return render(request, 'Homepage/task1.html')


def task2(request):
    return render(request, 'Homepage/task2.html')


def error(request):
    return render(request, 'Homepage/error_login.html')


def login2(request):
    return render(request, 'Homepage/Log_in.html')


def do_registration(request):
    return render(request, 'Homepage/registration.html')


def register(request):
    User.objects.create_user(
        request.POST['username'],
        password=request.POST['password'],
        first_name=' ',
        last_name=' ',
        email='',
    )
    return HttpResponseRedirect('/')


def login_user(request):
    user = authenticate(
        username=request.POST['username'],
        password=request.POST['password']
    )
    if user is None:
        pass
        return render(request, 'Homepage/error_login.html')
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

