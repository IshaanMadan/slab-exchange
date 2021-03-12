"""sport_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.urls import path,include
from se_app.views import *
urlpatterns = [
    path('login',UserLoginView.as_view()),
    path('card-image',ImageAPIVIEW.as_view()),
    path('data-status',DetailAPI.as_view()),
    path('save-card-details',savecarddetails.as_view()),
    path('get-form-list',getformlist.as_view()),
    path('delete-card/<str:card_id>',Deletecard.as_view()),



]