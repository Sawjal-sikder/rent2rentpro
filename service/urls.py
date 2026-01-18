
from django.urls import path # type: ignore
from service.views.contact_cration_views import ContactCreationView

urlpatterns = [
    path('contact-creation/', ContactCreationView.as_view(), name='contact-creation'),
]