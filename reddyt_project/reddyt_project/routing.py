from channels.auth import AuthMiddlewareStack
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
import notification_app.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            notification_app.routing.websocket_urlpatterns
        )
    ),
})
