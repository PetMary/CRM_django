import os
from datetime import datetime as date_t
import datetime

import dateutil.relativedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
import json

from .models import Services, Order, Customer

def ex(request):
    # data = Order.objects.filter(user=request.user.id)
    data1 = Order.objects.filter(user=request.user.id).order_by('-date_order')
    data = Order.objects.filter(user=request.user.id).order_by('-date_order').values('id', 'id_customer__name',
                                                                                    'id_services__name',
                                                                                    'date_order__date',
                                                                                    'date_order__time',
                                                                                    'id_services__price',)

    def json_date_handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    json_data = json.dumps(list(data), default=json_date_handler)

    name_ser = Services.objects.filter(user=request.user.id)
    return render(request, 'main_page/index.html', {'data': data1, 'json_data': json_data, 'name_ser': name_ser})


def home(request):
    return render(request, "main_page/home.html")


################################

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/singup.html"


# добавить параметр
def information_company(request, name):
    data = Services.objects.filter(user=request.user.id)  # поменять на определение по name
    return render(request, 'main_page/company.html', {'data': data})


@login_required(login_url='login')
def crm_information(request):
    data = Order.objects.filter(user=request.user.id).order_by('date_order')
    chart_1 = {}
    chart_2 = {}

    date_chart_1 = (datetime.date.today() - dateutil.relativedelta.relativedelta(months=4)).replace(day=1)
    date_chart = date_chart_1
    for i in range(5):
        chart_1[date_chart.strftime("%B")] = 0
        date_chart += dateutil.relativedelta.relativedelta(months=1)

    date_chart_1 = date_t.combine(date_chart_1, date_t.min.time())
    date_chart = date_t.combine(date_chart, date_t.min.time())
    for d in data:
        if d.date_order.timestamp() >= date_chart_1.timestamp() and d.date_order.timestamp() < date_chart.timestamp():
            chart_1[d.date_order.strftime("%B")] += 1
        try:
            chart_2[d.id_services.name] += 1
        except KeyError:
            chart_2[d.id_services.name] = 1
    new_chart_2 = list(map(list, chart_2.items()))
    new_chart_1 = list(map(list, chart_1.items()))

    try:
        with open("media/user_{0}/data_file_2.json".format(request.user.id), "w") as write_file:
            json.dump(new_chart_2, write_file)
        with open("media/user_{0}/data_file_1.json".format(request.user.id), "w") as write_file:
            json.dump(new_chart_1, write_file)
    except FileNotFoundError:
        os.mkdir("media/user_{0}".format(request.user.id))
        with open("media/user_{0}/data_file_2.json".format(request.user.id), "w") as write_file:
            json.dump(new_chart_2, write_file)
        with open("media/user_{0}/data_file_1.json".format(request.user.id), "w") as write_file:
            json.dump(new_chart_1, write_file)

    return render(request, 'main_page/dashboard.html', {'data': data})


@login_required(login_url='login')
def crm_orders(request):
    data1 = Order.objects.filter(user=request.user.id).order_by('-date_order')
    data = Order.objects.filter(user=request.user.id).order_by('-date_order').values('id', 'id_customer__name',
                                                                                     'id_services__name',
                                                                                     'date_order__date',
                                                                                     'date_order__time',
                                                                                     'id_services__price', )

    def json_date_handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    json_data = json.dumps(list(data), default=json_date_handler)

    name_ser = Services.objects.filter(user=request.user.id)
    return render(request, 'main_page/orders.html', {'data': data1, 'json_data': json_data, 'name_ser': name_ser})


@login_required(login_url='login')
def crm_customers(request):
    return HttpResponse('crm customers')


@login_required(login_url='login')
def crm_products(request):
    return HttpResponse('crm products')


def crm_redirect(request):
    return HttpResponseRedirect("/crm/dashboard")


def main_redirect(request):
    return HttpResponseRedirect("/")
