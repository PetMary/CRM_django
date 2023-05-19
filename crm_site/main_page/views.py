from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def main_page(request):
    return HttpResponse('main page')

def login(request):
    return HttpResponse('logon page')

# добавить параметр
def information_company(request, name):
    data = {"header": "Hello Django", "message": "Welcome to Python"}
    return render(request,'main_page/index2.html', context=data)

# обязательно логин
def crm_information(request):
    return render(request,'main_page/index.html')

def crm_orders(request):
    return HttpResponse('crm orders')

def crm_customers(request):
    return HttpResponse('crm customers')

def crm_products(request):
    return HttpResponse('crm products')

def crm_redirect(request):
    return HttpResponseRedirect("/crm/dashboard")

def main_redirect(request):
    return HttpResponseRedirect("/")