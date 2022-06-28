"""
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""

from django.urls import path
from . import views

urlpatterns = [
    path('agree/', views.AgreeViews.as_view(), name='agree'),
    path('checkme/', views.CheckmeViews.as_view(), name='checkme'),
    path('joinme/', views.JoinmeViews.as_view(), name='joinme'),
    path('joinok/', views.JoinokViews.as_view(), name='joinok'),
]
