# Generated by Django 3.1.5 on 2021-03-17 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizen', '0056_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='crime_category',
            name='cat_img',
            field=models.FileField(blank=True, default='default-pic.png', null=True, upload_to='images/'),
        ),
    ]
