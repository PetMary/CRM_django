import os
from datetime import datetime
import datetime as date_t_1
import dateutil.relativedelta
import pytz as pytz

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
from django.contrib import messages
import json

from .models import *
from django.contrib.auth.models import User


def delta_time(dt1, dt2):
    dt1 = dt1.astimezone(pytz.timezone('Europe/Moscow'))
    dt2 = dt2.astimezone(pytz.timezone('Europe/Moscow'))
    time_diff = dt1 - dt2
    time_diff = time_diff.total_seconds() // 60  # Разница в минутах
    time_diff = date_t_1.timedelta(minutes=time_diff)
    result_time = (datetime.min + time_diff).time()
    return result_time


def sum_time(dt1, dt2):
    dt1 = dt1.astimezone(pytz.timezone('Europe/Moscow'))
    dt2 = dt2.astimezone(pytz.timezone('Europe/Moscow'))
    result_datetime = dt1 + date_t_1.timedelta(hours=dt2.hour, minutes=dt2.minute, seconds=dt2.second)
    result_time = result_datetime.time()
    return result_time


@require_http_methods(["POST"])
def create_order(request):
    if request.method == 'POST':
        service_id = request.POST.get('service')
        service = Services.objects.get(id=service_id)
        status = Status.objects.get(id=3)

        try:
            customer_id = request.POST.get('customer')
            customer = Customer.objects.get(id=customer_id)
            user = User.objects.get(id=request.user.id)
        except:
            customer_name = request.POST.get('name')
            customer_phone = request.POST.get('phone')
            find_customer = Customer.objects.filter(phone=customer_phone)
            print(find_customer)
            if find_customer.count() == 0:
                customer = Customer.objects.create(name=customer_name, phone=customer_phone)
                customer.save()
            else:
                customer = find_customer[0]

            user = User.objects.get(id=service.id_employee.login_name.id)

        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        try:
            time = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            time = datetime.strptime(time_str, '%H:%M:%S').time()
        datetime_zone = datetime.combine(date, time)

        order = Order.objects.create(id_customer=customer, id_services=service, date_order=datetime_zone,
                                     id_status=status, user=user)
        order.save()
        print(order)
        messages.success(request, 'Запись сохранена.')

        # Перенаправьте пользователя на страницу с подтверждением или другую нужную вам страницу
        if request.user.is_authenticated:
            return HttpResponseRedirect("/crm/orders/")
        else:
            return HttpResponseRedirect(f"/company/{service.id_employee.id_company}")

    return render(request, 'main_page/order.html')


@require_http_methods(["POST"])
def find_time(request):
    service_id = request.POST.get('service')
    service = Services.objects.get(id=service_id)
    date_str = request.POST.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    try:
        employee = Employee.objects.get(id=service.id_employee.id)
        timetable = Timetable.objects.get(date=date, id_employee=employee.id)
        print('есть дата')

    except ObjectDoesNotExist:
        print('нет даты')
        response_data = {
            'date': date,
            'availableTime': 'Данная дата недоступна. Выберите другую дату.'
        }
        return JsonResponse(response_data)

    orders_day = Order.objects.filter(date_order__date=date, user=employee.login_name).order_by('date_order')

    time_start = timetable.start_day
    datetime_end = datetime.combine(date, timetable.end_day)
    datetime_start = datetime.combine(date, timetable.start_day)

    if orders_day.count() > 0:
        json_availableTime = []
        json_time = []
        for i in range(orders_day.count()):
            if i == 0:
                result_time = delta_time(orders_day[i].date_order, datetime_start)
                print('окно: ', result_time)
                if result_time >= service.time:
                    json_time.append(time_start)
                    json_availableTime.append(f'\nс {timetable.start_day} до '
                                              f'{(orders_day[i].date_order.astimezone(pytz.timezone("Europe/Moscow")).time())}')

            datetime_service = datetime.combine(date, orders_day[i].id_services.time)
            result_datetime = datetime.combine(date, sum_time(orders_day[i].date_order, datetime_service))
            if i == orders_day.count() - 1:
                result_time = delta_time(datetime_end, result_datetime)
                print('окно: ', result_time)
                if result_time >= service.time:
                    json_time.append(result_datetime.time())
                    json_availableTime.append(f'\nс {result_datetime.time()} до {datetime_end.time()}')
            else:
                result_time = delta_time(orders_day[i + 1].date_order, result_datetime)
                print('окно: ', result_time)
                if result_time >= service.time:
                    json_time.append(result_datetime.time())
                    json_availableTime.append(f'\nс {result_datetime.time()} до '
                                              f'{(orders_day[i + 1].date_order.astimezone(pytz.timezone("Europe/Moscow")).time())}')
    else:
        datetime_delta = datetime.combine(date, service.time)
        time_end_order = datetime_end - datetime_delta

        response_data = {
            'time': time_start,
            'date': date,
            'availableTime': f'\nс {timetable.start_day} до {time_end_order}'  # Пример доступного времени
        }

        return JsonResponse(response_data)

    if len(json_time) > 0:
        response_data = {
            'time': json_time[0],
            'date': date,
            'availableTime': json_availableTime
        }

        return JsonResponse(response_data)
    else:
        response_data = {
            'date': date,
            'availableTime': 'На выбранную дату нет свободного времени'
        }

        return JsonResponse(response_data)


def ex(request):
    # data = Order.objects.filter(user=request.user.id)
    customers = BaseCustomer.objects.filter(user=request.user.id).values('id_customer', 'id_customer__name', )
    services = Services.objects.filter(user=request.user.id)

    return render(request, 'main_page/index.html', {'services': services, 'customers': customers})

################################


def home(request):
    return render(request, "main_page/home.html")


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/singup.html"


def information_company(request, name):
    try:
        company = Company.objects.get(name=name)
        data = Services.objects.filter(id_employee__id_company__name=name)

        return render(request, 'main_page/company.html', {'data': data})
    except ObjectDoesNotExist:
        return main_redirect(request)


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
