from django.urls import path

from orders.api import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.CreateOrderAPIView.as_view(), name='create'),
    path('<str:lookup>/', views.RetrieveUpdateOrderAPIView.as_view(), name='order'),
]
