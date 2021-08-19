from django.urls import path

from operations import views

urlpatterns = [
    path('', views.index, name="home"),
    path('buy/', views.buy, name="buy"),
    path('sell/', views.sell, name="sell"),
    path('history', views.history, name="history")
]