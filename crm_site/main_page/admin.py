from django.contrib import admin
from .models import Customer, Week, Status, Services, Timetable, Order, Employee, Direction, Company, \
    BaseCustomer, Book

# Register your models here.
admin.site.register(Customer)
admin.site.register(Week)
admin.site.register(Status)
admin.site.register(Services)
admin.site.register(Timetable)
admin.site.register(Order)
admin.site.register(Employee)
admin.site.register(Direction)
admin.site.register(Company)
admin.site.register(BaseCustomer)

admin.site.register(Book)
