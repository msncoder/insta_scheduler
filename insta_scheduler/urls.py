"""
URL configuration for insta_scheduler project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from core import views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('facebook-login/', views.facebook_login, name='facebook_login'),
    path('facebook-callback/', views.facebook_callback, name='facebook_callback'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('privacy-policy/', TemplateView.as_view(template_name="core/privacy_policy.html"), name='privacy_policy'),
    path('data-deletion/', TemplateView.as_view(template_name="core/data_deletion.html"), name='data_deletion'),

]

