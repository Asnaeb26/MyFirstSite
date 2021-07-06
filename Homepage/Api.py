import requests
import json
import datetime as dt


def get_response():
    now = str(dt.date.today())
    day = str(int(now.split('-')[-1]) - 6)
    # print(day)
    response = requests.get('https://www.nbrb.by/api/exrates/rates/dynamics/145?startdate=2021-06-' + day + '&enddate='+ now)
    data = json.loads(response.text)
    sum = 0
    for i in data:
        current_date = i['Date'].split('T')[0]
        date_course = i['Cur_OfficialRate']
        # print(curse_date)
        day = current_date.split('-')[-1]
        month = current_date.split('-')[1]
        year = current_date.split('-')[0]
        sum += float(date_course)
        # print(f'Курс доллара на {day}.{month}.{year} - {date_course} BYN')
    print(f'Среднее значение за неделю составит {(sum / 7 )} BYN')
    # print(now)
    # print(data)
    # print(data[0])


get_response()