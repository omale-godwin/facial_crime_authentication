# Generated by Django 2.2.2 on 2019-07-12 14:50

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.CharField(default='emp319', max_length=70, unique=True)),
                ('thumb', models.ImageField(blank=True, upload_to='')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=125)),
                ('emergency', models.CharField(max_length=11)),
                ('gender', models.CharField(max_length=10)),
                ('joined', models.DateTimeField(default=datetime.datetime(2019, 7, 12, 14, 50, 15, 657294, tzinfo=utc))),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hrms.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('first_in', models.TimeField(auto_now_add=True)),
                ('last_out', models.TimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PRESENT', 'PRESENT'), ('ABSENT', 'ABS'), ('UNAVAILABLE', 'UNAVAIL')], max_length=15)),
                ('staff', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hrms.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumb', models.ImageField(blank=True, default='avatar2.png', upload_to='')),
                ('user', models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
