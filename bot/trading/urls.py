from django.urls import path

from trading import views

urlpatterns = [
    path('', views.index, name="home"),
    path('user/', views.userPage, name="user_page"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    # CRUDL
    path('add_order/', views.trading_history_create, name="add_order"),
    path('edit_order/<int:pk>', views.trading_history_update, name="edit_order"),
    path('delete_order/<int:pk>', views.trading_history_delete, name="delete_order"),
    path('close_order/<int:pk>', views.trading_history_close, name="close_order"),
]