from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

# if settings.DEBUG:
#     urlpatterns += [
#         re_path(r'^media/(?P<path>.*)$', serve, {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#     ]
