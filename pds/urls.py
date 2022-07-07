"""
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""

from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ListView.as_view(), name='plist'),
    path('modify/', views.ModifyView.as_view(), name='pmodify'),
    path('view/', views.ViewView.as_view(), name='pview'),
    path('write/', views.WriteView.as_view(), name='pwrite'),
    path('remove/', views.RemoveView.as_view(), name='premove'),
    path('pdown/', views.PdownView.as_view(), name='pdown'),
]

