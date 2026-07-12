from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/students/', include('students.urls')),
    path('api/faculty/', include('faculty.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/leave/', include('leave.urls')),
    path('api/results/', include('results.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
