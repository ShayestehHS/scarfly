from django.urls import path

from orders.api import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.CreateOrderAPIView.as_view(), name='create'),
    path('list/', views.ListOrderAPIView.as_view(), name='list'),
    path('retrieve/<str:lookup>/', views.RetrieveOrderAPIView.as_view(), name='retrieve'),
    path('update/status/<str:lookup>/', views.UpdateOrderStatusAPIView.as_view(), name='update'),
]
