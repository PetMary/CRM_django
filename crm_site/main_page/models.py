from django.db import models

class BaseCustomer(models.Model):
    id_customer = models.ForeignKey('Customer', on_delete=models.CASCADE, db_column='id_customer')
    id_company = models.ForeignKey('Company', on_delete=models.CASCADE, db_column='id_company')
    start_day = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_customer'
        unique_together = (('id_customer', 'id_company'),)


class Company(models.Model):
    id_direction = models.ForeignKey('Direction', on_delete=models.CASCADE, db_column='id_direction')
    name = models.CharField()
    description = models.TextField(blank=True, null=True)
    address = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'


class Customer(models.Model):
    name = models.CharField()
    surname = models.CharField()
    patronymic = models.CharField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    phone = models.CharField()

    class Meta:
        managed = False
        db_table = 'customer'


class Direction(models.Model):
    name = models.CharField()

    class Meta:
        managed = False
        db_table = 'direction'

class Employee(models.Model):
    id_company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='id_company')
    name = models.CharField()
    surname = models.CharField()
    patronymic = models.CharField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    phone = models.CharField()

    class Meta:
        managed = False
        db_table = 'employee'

class Order(models.Model):
    id_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='id_customer')
    id_services = models.ForeignKey('Services', on_delete=models.CASCADE, db_column='id_services')
    date_order = models.DateTimeField()
    id_status = models.ForeignKey('Status', on_delete=models.CASCADE, db_column='id_status')
    sum_price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'order'


class Services(models.Model):
    id_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='id_employee')
    name = models.CharField()
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    time = models.TimeField()
    image = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'services'


class Status(models.Model):
    name = models.CharField()

    class Meta:
        managed = False
        db_table = 'status'


class Timetable(models.Model):
    id_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='id_employee')
    id_week = models.ForeignKey('Week', on_delete=models.CASCADE, db_column='id_week')
    start_day = models.TimeField()
    end_day = models.TimeField()
    break_time = models.TimeField()

    class Meta:
        managed = False
        db_table = 'timetable'
        unique_together = (('id_employee', 'id_week'),)


class Week(models.Model):
    name = models.CharField()

    class Meta:
        managed = False
        db_table = 'week'
