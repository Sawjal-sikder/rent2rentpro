from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from django.views.static import serve   # type: ignore
from django.urls import re_path # type: ignore
from django.conf import settings    # type: ignore
from django.conf.urls.static import static # type: ignore
from django.http import JsonResponse # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/user/', include('user_profile.urls')),
    path('accounts/', include('allauth.urls')),
    path('', lambda request: JsonResponse({
        "status": "success",
        "service": "Welcome to Violet Backend API",
        "message": "Service is operational"
    })),

]


urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

def custom_404_handler(request, exception):
    return JsonResponse({"error": "Invalid URL, please correct the URL"}, status=404)

handler404 = custom_404_handler