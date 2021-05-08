from django.urls import path, reverse

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("login/", views.login, name="login"),
    path('ranks/<int:list_id>/', views.rankview, name='ranklist'),
    path('ranks/<int:list_id>/add-item/', views.new_item, name='new-item'),
    path('ranks/<int:list_id>/vote', views.VoteView.as_view(), name='vote'),
    path('new-list/', views.add_new_list, name='new-list'),
    path('awesome-baby/', views.awesome_baby, name='awesome-baby'),
    path('data-from-ajax/', views.data_from_ajax, name='data-from-ajax'),
    path('api/ranks/<int:list_id>/', views.data_only_view, name='data-only-view'),
]
