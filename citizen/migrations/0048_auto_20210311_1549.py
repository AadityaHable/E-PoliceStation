# Generated by Django 3.1.5 on 2021-03-11 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizen', '0047_complaint_complaint_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='gender',
            field=models.CharField(max_length=10),
        ),
    ]
