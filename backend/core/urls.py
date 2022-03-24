"""scarfly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')), # Fake admin url
    path('scarf_admin_ly/', admin.site.urls),
    path('accounts/', include('accounts.api.urls', namespace='accounts')),
    path('orders/', include('orders.api.urls', namespace='orders')),
    path('products/', include('products.api.urls', namespace='products')),
]
if settings.DEBUG:
    from debug_toolbar import urls as debug_toolbar_url

    urlpatterns += [path('__debug__/', include(debug_toolbar_url))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
