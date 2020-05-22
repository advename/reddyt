from django.urls import path
from . import api_views


app_name = "notification_app_api"

# explanation of urlpatterns down below
urlpatterns = [
    path("unread/",
         api_views.UnreadNotification.as_view(), name="unread_notif"),
]
