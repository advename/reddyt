from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import include, path  # add include to the import apps

app_name = "api_app"

urlpatterns = [
    path("discussion/", include('discussion_app.api_urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)