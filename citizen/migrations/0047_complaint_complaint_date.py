# Generated by Django 3.1.5 on 2021-03-11 10:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('citizen', '0046_auto_20210311_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='complaint_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
