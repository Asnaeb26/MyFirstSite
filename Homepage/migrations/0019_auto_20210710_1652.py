# Generated by Django 3.2.3 on 2021-07-10 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0018_person3'),
    ]

    operations = [
        migrations.AddField(
            model_name='spentmoney',
            name='category',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='spentmoney',
            name='comments',
            field=models.TextField(max_length=100),
        ),
    ]