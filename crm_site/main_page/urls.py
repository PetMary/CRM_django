from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from . import views

crm_patterns = [
    path("", views.crm_redirect, name='dashboard_redirect'),
    path("dashboard/", views.crm_information, name='dashboard'),
    path("orders/", views.crm_orders, name='orders'),
    path("customers/", views.crm_customers, name='customers'),
    path("products/", views.crm_products, name='products'),

    path('create_order/', views.create_order, name='create_order'),
]

urlpatterns = [
    path('ex/', views.ex, name='ex'),

    path('', views.home, name="home"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('company/', views.main_redirect, name='main_redirect'),
    path('company/<str:name>', views.information_company, name='information_company'),
    path('crm/', include(crm_patterns)),
    # path('crm/dashboard/', views.crm_information, name='crm_main'), # ИЛИ company/name/dashboard
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
