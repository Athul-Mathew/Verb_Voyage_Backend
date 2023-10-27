import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'verbvoyage.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from .routing import websocket_urlpatterns
django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': (
        URLRouter(routes=websocket_urlpatterns)
    )

})