from django.urls import path, include
from . import views

crm_patterns = [
    path("", views.crm_redirect, name='dashboard_redirect'),
    path("dashboard/", views.crm_information, name='dashboard'),
    path("orders/", views.crm_orders, name='orders'),
    path("customers/", views.crm_customers, name='customers'),
    path("products/", views.crm_products, name='products'),
]

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('company/', views.main_redirect, name='main_redirect'),
    path('company/<str:name>', views.information_company, name='information_company'), #изменить int на str название компании
    path('login/', views.login, name='login'),
    path('crm/', include(crm_patterns)),
    # path('crm/dashboard/', views.crm_information, name='crm_main'), # ИЛИ company/name/dashboard
]