from django.db import models
import sqlite3


class Person3(models.Model):
    name = models.CharField(
        max_length=100
    )
    age = models.IntegerField(
        default=18
    )
    credit_card_number = models.CharField(
        max_length=90
    )


class SpentMoney(models.Model):
    add_money = models.FloatField(default=0)
    comments = models.TextField(max_length=100)
    time_input = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)



class Randomiser(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(default=0)


