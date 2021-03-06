from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('definitive.urls')),
    path('admin/', admin.site.urls),
    path('social-auth/', include('social_django.urls', namespace="social")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

