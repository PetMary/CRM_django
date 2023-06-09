# Generated by Django 4.2.1 on 2023-05-20 22:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main_page.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('address', models.CharField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, null=True)),
                ('surname', models.CharField(blank=True, null=True)),
                ('patronymic', models.CharField(blank=True, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('email', models.CharField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, null=True)),
                ('surname', models.CharField(blank=True, null=True)),
                ('patronymic', models.CharField(blank=True, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('email', models.CharField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, null=True)),
                ('login_name', models.CharField()),
                ('id_company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_page.company')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('image', models.ImageField(upload_to=main_page.models.user_directory_path)),
                ('id_employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_page.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_order', models.DateTimeField(blank=True, null=True)),
                ('sum_price', models.IntegerField(blank=True, null=True)),
                ('id_customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_page.customer')),
                ('id_services', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_page.services')),
                ('id_status', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_page.status')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='id_direction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_page.direction'),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('cover', models.ImageField(upload_to=main_page.models.user_directory_path)),
                ('book', models.FileField(upload_to='books/')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_day', models.TimeField(blank=True, null=True)),
                ('end_day', models.TimeField(blank=True, null=True)),
                ('break_time', models.TimeField(blank=True, null=True)),
                ('id_employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_page.employee')),
                ('id_week', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_page.week')),
            ],
            options={
                'unique_together': {('id_employee', 'id_week')},
            },
        ),
        migrations.CreateModel(
            name='BaseCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_day', models.DateField(blank=True, null=True)),
                ('id_company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_page.company')),
                ('id_customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_page.customer')),
            ],
            options={
                'unique_together': {('id_customer', 'id_company')},
            },
        ),
    ]
