# Generated by Django 3.2.3 on 2021-09-28 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0030_delete_person3'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=40)),
                ('alias', models.TextField(max_length=40)),
            ],
        ),
    ]
