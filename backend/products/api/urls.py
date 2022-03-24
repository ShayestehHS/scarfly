from django.urls import path

from products.api import views

app_name = 'products'

urlpatterns = [
    path('<int:pro_code>/', views.RetrieveProductAPIView.as_view(), name='retrieve'),
]
