import json
import datetime
import requests
from Homepage.models import Client, User


def date(request):
    DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    client = Client.objects.filter(user_id=request.user.id)[0]
    current_year = datetime.date.today().year
    current_month = datetime.date.today().month
    direction = request.GET.get('direction')
    month = request.GET.get('month')
    if direction == 'next':
        current_month = int(month) + 1
        if current_month == len(DAYS_IN_MONTH):
            current_month = 1
            current_year += 1
    elif direction == 'back':
        current_month = int(month) - 1
        if current_month < 1:
            current_month = 12
            current_year -= 1
    if client.set_day > DAYS_IN_MONTH[current_month]:
        selected_day = DAYS_IN_MONTH[current_month]
    else:
        selected_day = client.set_day
    first_day = datetime.date(current_year, current_month, selected_day)
    next_month = current_month + 1
    if next_month >= len(DAYS_IN_MONTH):
        next_month = 1
    last_day = first_day + datetime.timedelta(days=DAYS_IN_MONTH[next_month])
    return first_day, last_day, current_month


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


def exchange_rates():
    response = requests.get('https://www.nbrb.by/api/exrates/rates/431')
    data = json.loads(response.text)
    dollar = data['Cur_OfficialRate']
    abbr = data['Cur_Abbreviation']
    return dollar, abbr
