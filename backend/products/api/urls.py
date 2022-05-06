from django.urls import path

from products.api import views

app_name = 'products'

urlpatterns = [
    path('retrieve/<int:pro_code>/', views.RetrieveProductAPIView.as_view(), name='retrieve'),
    path('list/', views.ListProductAPIView.as_view(), name='list'),
]
