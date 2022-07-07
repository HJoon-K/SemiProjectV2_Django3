"""
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""

from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ListView.as_view(), name='glist'),
    path('modify/', views.ModifyView.as_view(), name='gmodify'),
    path('view/', views.ViewView.as_view(), name='gview'),
    path('write/', views.WriteView.as_view(), name='gwrite'),
    path('remove/', views.RemoveView.as_view(), name='gremove'),
]

