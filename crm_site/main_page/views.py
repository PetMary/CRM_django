import os
from datetime import datetime
import datetime as date_t_1
import dateutil.relativedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
from django.contrib import messages
import json

from .models import Services, Order, Customer, BaseCustomer, Status
from django.contrib.auth.models import User

@require_http_methods(["POST"])
def create_order(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        customer = Customer.objects.get(id=customer_id)
        service_id = request.POST.get('service')
        service = Services.objects.get(id=service_id)
        status = Status.objects.get(id=3)
        user = User.objects.get(id=request.user.id)

        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M').time()

        order = Order.objects.create(id_customer=customer, id_services=service, date_order=datetime.combine(date, time),
                                     id_status=status, user=user)
        order.save()
        print(order)
        messages.success(request, 'Заказ сохранен.')

        # Перенаправьте пользователя на страницу с подтверждением или другую нужную вам страницу
        return HttpResponseRedirect("/crm/orders/")

    return render(request, 'main_page/order.html')


def ex(request):
    # data = Order.objects.filter(user=request.user.id)
    customers = BaseCustomer.objects.filter(user=request.user.id).values('id_customer', 'id_customer__name', )
    services = Services.objects.filter(user=request.user.id)

    return render(request, 'main_page/index.html', {'services': services, 'customers' : customers})

################################


def home(request):
    return render(request, "main_page/home.html")


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

    date_chart_1 = (date_t_1.date.today() - dateutil.relativedelta.relativedelta(months=4)).replace(day=1)
    date_chart = date_chart_1
    for i in range(5):
        chart_1[date_chart.strftime("%B")] = 0
        date_chart += dateutil.relativedelta.relativedelta(months=1)

    date_chart_1 = datetime.combine(date_chart_1, datetime.min.time())
    date_chart = datetime.combine(date_chart, datetime.min.time())
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

    customers = BaseCustomer.objects.filter(user=request.user.id).values('id_customer', 'id_customer__name', )
    services = Services.objects.filter(user=request.user.id)

    return render(request, 'main_page/orders.html', {'data': data1, 'json_data': json_data, 'name_ser': name_ser,
                                                     'services': services, 'customers': customers})


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
