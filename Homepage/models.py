from django.db import models
import sqlite3


class User(models.Model):
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    time_create = models.DateTimeField(auto_now_add=True)


class Person3(models.Model):
    name = models.CharField(
        max_length=100
    )
    credit_card_number = models.CharField(
        max_length=90
    )


class SpentMoney(models.Model):
    add_money = models.IntegerField(default=0)
    comments = models.TextField(max_length=255)
    time_input = models.DateTimeField(auto_now_add=True)