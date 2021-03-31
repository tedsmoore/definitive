from django.urls import path, reverse
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ranks/<int:list_id>/', views.rankview, name='ranklist'),
    path('ranks/<int:list_id>/add-item/', views.new_item, name='new-item')
]
