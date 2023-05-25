from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

def user_directory_path(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class BaseCustomer(models.Model):
    id_customer = models.ForeignKey('Customer', models.DO_NOTHING)
    id_company = models.ForeignKey('Company', models.DO_NOTHING)
    start_day = models.DateField(blank=True, null=True)
    user = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.id_customer.name} - {self.id_company.name}"

    class Meta:
        unique_together = ('id_customer', 'id_company')


class Company(models.Model):
    id_direction = models.ForeignKey('Direction', models.DO_NOTHING)
    name = models.CharField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(blank=True, null=True)
    surname = models.CharField(blank=True, null=True)
    patronymic = models.CharField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.name


class Direction(models.Model):
    name = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    id_company = models.ForeignKey(Company, models.DO_NOTHING)
    name = models.CharField(blank=True, null=True)
    surname = models.CharField(blank=True, null=True)
    patronymic = models.CharField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True)
    login_name = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Order(models.Model):
    id_customer = models.ForeignKey(Customer, models.DO_NOTHING)
    id_services = models.ForeignKey('Services', models.DO_NOTHING)
    date_order = models.DateTimeField(blank=True, null=True)
    id_status = models.ForeignKey('Status', models.DO_NOTHING)
    # sum_price = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.id_customer.name} - {self.id_services.name}"

    def is_notend(self):
        return self.date_order.timestamp() >= datetime.now().timestamp()


class Services(models.Model):
    id_employee = models.ForeignKey(Employee, models.DO_NOTHING)
    name = models.CharField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    user = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to=user_directory_path)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.name


class Timetable(models.Model):
    id_employee = models.ForeignKey(Employee, models.DO_NOTHING)
    id_week = models.ForeignKey('Week', models.DO_NOTHING)
    start_day = models.TimeField(blank=True, null=True)
    end_day = models.TimeField(blank=True, null=True)
    break_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.id_employee.name} - {self.id_week.name}"

    class Meta:
        unique_together = ('id_employee', 'id_week')


class Week(models.Model):
    name = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.name
