"""
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""

from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ListView.as_view(), name='blist'),
    path('modify/', views.ModifyView.as_view(), name='bmodify'),
    path('view/', views.ViewView.as_view(), name='bview'),
    path('write/', views.WriteView.as_view(), name='bwrite'),
    path('remove/', views.RemoveView.as_view(), name='bremove'),
    path('setup/', views.SetupView.as_view(), name='bsetup'),
]

