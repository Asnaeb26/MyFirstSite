# Generated by Django 3.2.3 on 2021-08-06 21:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0026_income'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='time_input',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
