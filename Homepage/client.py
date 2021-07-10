# from Homepage.models import User
import requests


# Сделать rest api для таблицы Человек.
# Поля таблицы: имя, возраст
#
# api должно следовать правилам 1 2 3 4
# Приделать валидации - возраст число, имя не число, имя больше 3-х букв.
# Написать тесты работы api. Клиент должен уметь кэшировать (смотри правило 3).
# Клиент должен юзать библиотеку requests.


def client():
    request.post(
        'http://127.0.0.1:8000/get_user',
        {
            'id': 1,
            'name': 'Олег',
            'age': 31
        }
    )


def get():
    g = requests.get('http://127.0.0.1:8000/get_user?id=1')
    print(g.text)

get()