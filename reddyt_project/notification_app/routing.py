from django.urls import path, include
from channels.routing import URLRouter
from . import consumers


websocket_urlpatterns = [
    path('ws/notifications/', consumers.NotificationConsumer),
]
