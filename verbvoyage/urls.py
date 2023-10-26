
from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView
from . import routing
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('Accounts.urls')),
    path('api/mentors/',include('mentors.urls')),
    path('api/subscription/',include('subscription.urls')),
    path('api/chat/', include('chat.urls')),
   

    #  path('api/chat', include(router.urls)),
    path('ws/', include(routing.websocket_urlpatterns)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


