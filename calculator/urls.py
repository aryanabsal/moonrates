from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get-price/<str:currency>/", views.get_crypto_price, name='get_price'),
    path("convert-currency/", views.convert_currency, name='convert_currency'),
    path("news/", views.news, name='news'),
    path("services/", views.services, name='services'),
    path("about/", views.about, name='about'),
    path('market-data/', views.market_data, name='market_data'),

]
