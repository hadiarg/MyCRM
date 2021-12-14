from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('account/', views.account, name="account"),
    path('customer/<str:pk_test>', views.customer, name="customer"),
    path('update_order/<str:pk>', views.update_order, name="update_order"),
    path('create_order/<str:pk>', views.create_order, name="create_order"),
    path('delete_order/<str:pk>', views.delete_Order, name="delete_order"),
    path('logout/', views.LogoutUser, name="logout"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('reset_password/', views.reset_password, name="reset_password"),
]