import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import newapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(newapp.routing.websocket_urlpatterns)
    ),
})