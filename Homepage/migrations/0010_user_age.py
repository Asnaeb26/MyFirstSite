# Generated by Django 3.2.3 on 2021-07-09 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0009_alter_spentmoney_add_money'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=18),
        ),
    ]
