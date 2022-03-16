from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include(('authentication.urls', 'authentication'), namespace='authentication')),
    path('', include(('books.urls', 'books'), namespace='books'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
