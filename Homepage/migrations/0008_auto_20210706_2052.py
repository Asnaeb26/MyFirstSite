# Generated by Django 3.2.3 on 2021-07-06 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0007_auto_20210706_2049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person3',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='person3',
            name='salary',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]