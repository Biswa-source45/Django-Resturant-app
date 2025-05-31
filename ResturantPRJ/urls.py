"""
URL configuration for ResturantPRJ project.

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
from core.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', about, name='about'),
    path('order/',order_history,name='order_history'),
    path('chef/',chefs,name='chefs'),
    path('login/', login_page, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('',home,name='home'),
    path('menu/',menu,name='menu'),
    path('menu/<int:id>/', menu_detail, name='menu_detail'),
    path('order/<int:id>/', order_confirm, name='order_confirm'),
    path('invoice/<str:order_number>/', invoice, name='invoice'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
