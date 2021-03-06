"""
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeViews.as_view(), name='index'),
    path('intro/', views.IntroViews.as_view(), name='intro'),
    path('admin/', views.AdminViews.as_view(), name='admin'),
    path('login/', views.LoginViews.as_view(), name='login'),
    path('loginfail/', views.LoginfailViews.as_view(), name='loginfail'),
    path('logout/', views.LogoutViews.as_view(), name='logout'),

]

