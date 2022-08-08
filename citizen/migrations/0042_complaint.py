# Generated by Django 3.1.5 on 2021-03-11 09:22

import citizen.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('citizen', '0041_delete_complaint'),
    ]

    operations = [
        migrations.CreateModel(
            name='complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50, validators=[citizen.models.commissionerfvalidation])),
                ('lastname', models.CharField(max_length=50, validators=[citizen.models.commissionerlvalidation])),
                ('contact_no', models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format of intergers only . Up to 10 digits allowed.', regex='^\\+?1?\\d{10}$')])),
                ('complaint_title', models.CharField(max_length=50)),
                ('complaint_description', models.CharField(max_length=500)),
                ('complaint_no', models.CharField(max_length=100)),
                ('proof_img', models.FileField(upload_to='images/')),
                ('proof_video', models.FileField(null=True, upload_to='videos/', verbose_name='video file')),
                ('address', models.CharField(blank=True, max_length=500)),
                ('gender', models.CharField(choices=[('M', 'MALE'), ('F', 'FEMALE')], max_length=10)),
                ('dob', models.DateField(blank=True)),
                ('citizen_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citizen.citizen')),
            ],
        ),
    ]
