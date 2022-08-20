"""Bww_v1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from inventory.views import RequestResetEmailView,SetNewPasswordView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('inventory.urls')),
    path('',include('purchase.urls')),
    path('',include('sales.urls')),
    path('',include('dispatch.urls')),
    
    
       #Reset screen with email field
    path('password_reset/',RequestResetEmailView.as_view(),name='password_reset'),

    #After sending the mail this view will appear 

    #This runs in backend to generate token and send mails
    path('reset/<uidb64>/<token>/',SetNewPasswordView.as_view(),name='password_reset_confirm'),

#internal
     
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
    
      


