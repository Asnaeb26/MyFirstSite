from django.db import models
from django.contrib.auth.models import User
import sqlite3


class SpentMoney(models.Model):
    add_money = models.FloatField(default=0)
    comments = models.TextField(max_length=100)
    category = models.CharField(max_length=100)
    time_input = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Income(models.Model):
    add_income = models.FloatField(default=0)
    comment = models.TextField(max_length=40)
    source = models.CharField(max_length=40)
    time_input = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Client(models.Model):
    avatar = models.ImageField()
    set_day = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

