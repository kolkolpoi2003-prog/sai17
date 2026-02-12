from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('fitting-request/', views.fitting_request, name='fitting_request'),
    path('product/<slug:slug>/quick-view/', views.quick_view, name='quick_view'),
]
