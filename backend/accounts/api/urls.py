from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.api import views

app_name = 'accounts'

urlpatterns = [
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('verify/', views.Verify.as_view(), name='verify'),
    path('retrieve/', views.RetrieveUpdateUserAPIView.as_view(), name='retrieve'),
    path('update/', views.RetrieveUpdateUserAPIView.as_view(), name='update'),
]
