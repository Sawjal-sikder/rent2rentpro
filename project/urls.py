from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from django.views.static import serve   # type: ignore
from django.urls import re_path # type: ignore
from django.conf import settings    # type: ignore
from django.conf.urls.static import static # type: ignore
from django.http import JsonResponse # type: ignore
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
) # type: ignore
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/user/', include('user_profile.urls')),
    path('api/v1/service/', include('service.urls')),
    path('api/v1/payment/', include('payment.urls')),
    
    # others apps
    path('accounts/', include('allauth.urls')),
    path('', lambda request: JsonResponse({
        "status": "success",
        "service": "Welcome to rent2rent Backend API",
        "message": "Service is operational"
    })),
    
    # Documentation URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]



urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

def custom_404_handler(request, exception):
    return JsonResponse({"error": "Invalid URL, please correct the URL"}, status=404)

handler404 = custom_404_handler