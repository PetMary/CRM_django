import os
import datetime
import dateutil.relativedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
import json

from .models import Services, Order, Customer


def ex(request):
    # data = Order.objects.filter(user=request.user.id)
    data = Services.objects.filter(user=request.user.id)  # поменять на определение по name
    return render(request, 'main_page/index.html', {'data': data})
    # добавить для второго графика
    # chart_2 = {}
    # for d in data:
    #     try:
    #         chart_2[d.id_services.name] += 1
    #     except KeyError:
    #         chart_2[d.id_services.name] = 1
    # new_chart_2 = list(map(list, chart_2.items()))
    #
    # try:
    #     with open("media/user_{0}/data_file.json".format(request.user.id), "w") as write_file:
    #         json.dump(new_chart_2, write_file)
    # except FileNotFoundError:
    #     os.mkdir("media/user_{0}".format(request.user.id))
    #     with open("media/user_{0}/data_file.json".format(request.user.id), "w") as write_file:
    #         json.dump(new_chart_2, write_file)

    # return render(request, "main_page/index.html", {'data': data})


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
    data = Order.objects.filter(user=request.user.id)
    chart_1 = {}
    chart_2 = {}

    date_chart_1 = (datetime.date.today() - dateutil.relativedelta.relativedelta(months=4)).replace(day=1)
    date_chart = date_chart_1
    for i in range(5):
        chart_1[date_chart.strftime("%B")] = 0
        date_chart += dateutil.relativedelta.relativedelta(months=1)

    date_chart_1 = datetime.datetime.combine(date_chart_1, datetime.datetime.min.time())
    date_chart = datetime.datetime.combine(date_chart, datetime.datetime.min.time())
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

    return render(request, 'main_page/dashbord.html',{'data': data})


@login_required(login_url='login')
def crm_orders(request):
    return HttpResponse('crm orders')


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
