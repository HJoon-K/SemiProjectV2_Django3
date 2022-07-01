"""
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""

from django.urls import path
from . import views

urlpatterns = [
    path('agree/', views.AgreeView.as_view(), name='agree'),
    path('checkme/', views.CheckmeView.as_view(), name='checkme'),
    path('joinme/', views.JoinmeView.as_view(), name='joinme'),
    path('joinok/', views.JoinokView.as_view(), name='joinok'),
    path('zipcode/', views.ZipcodeView.as_view(), name='zipcode'),
    path('userid/', views.UseridView.as_view(), name='userid'),
]
