# Generated by Django 3.1.5 on 2021-03-18 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizen', '0065_fir_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizen',
            name='gender',
            field=models.CharField(max_length=10),
        ),
    ]
