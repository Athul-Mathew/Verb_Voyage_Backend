# chat/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('send_message/', MessageViewSet.as_view({'post': 'send_message'}), name='send_message'),
    path('get_messages/<int:user_id>/<int:mentor_id>/', get_messages, name='get_messages'),
    path('users/<int:mentor_id>/', get_mentor_users, name='get_users_with_messages'), 
]