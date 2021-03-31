from django.urls import path

from . import views

urlpatterns = [
    path('ranks/<int:list_id>/', views.rankview, name='index'),
    path('ranks/<int:list_id>/add-item/', views.new_item, name='new-item')
]

# if settings.DEBUG:
#     urlpatterns += [
#         re_path(r'^media/(?P<path>.*)$', serve, {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#     ]
