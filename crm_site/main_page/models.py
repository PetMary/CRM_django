# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BaseCustomer(models.Model):
    id_customer = models.ForeignKey('Customer', models.DO_NOTHING, db_column='id_customer')
    id_company = models.ForeignKey('Company', models.DO_NOTHING, db_column='id_company')
    start_day = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_customer'
        unique_together = (('id_customer', 'id_company'),)


class Company(models.Model):
    id_direction = models.ForeignKey('Direction', models.DO_NOTHING, db_column='id_direction')
    name = models.CharField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'


class Customer(models.Model):
    name = models.CharField(blank=True, null=True)
    surname = models.CharField(blank=True, null=True)
    patronymic = models.CharField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'


class Direction(models.Model):
    name = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'direction'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employee(models.Model):
    id_company = models.ForeignKey(Company, models.DO_NOTHING, db_column='id_company')
    name = models.CharField(blank=True, null=True)
    surname = models.CharField(blank=True, null=True)
    patronymic = models.CharField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee'


class HelloNews(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'hello_news'


class Order(models.Model):
    id_customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='id_customer')
    id_services = models.ForeignKey('Services', models.DO_NOTHING, db_column='id_services')
    date_order = models.DateTimeField(blank=True, null=True)
    id_status = models.ForeignKey('Status', models.DO_NOTHING, db_column='id_status')
    sum_price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order'


class Services(models.Model):
    id_employee = models.ForeignKey(Employee, models.DO_NOTHING, db_column='id_employee')
    name = models.CharField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    image = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'services'


class Status(models.Model):
    name = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status'


class Timetable(models.Model):
    id_employee = models.ForeignKey(Employee, models.DO_NOTHING, db_column='id_employee')
    id_week = models.ForeignKey('Week', models.DO_NOTHING, db_column='id_week')
    start_day = models.TimeField(blank=True, null=True)
    end_day = models.TimeField(blank=True, null=True)
    break_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timetable'
        unique_together = (('id_employee', 'id_week'),)


class Week(models.Model):
    name = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'week'
