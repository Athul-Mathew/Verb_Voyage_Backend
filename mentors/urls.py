from django.urls import path,include
from . import views
# from.routing import websocket_urlpatterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [

    
    path('mentors/', views.get_mentors, name='get_mentors'),
    path('mentors/<int:id>', views.mentorView, name='get_mentors'),
    path('mentor-application/', views.mentor_application_view, name='mentor-application'),
    path('view-mentors/',views.view_mentors,name='view_mentors'),
    path('view-mentors-request/',views.view_mentors_request,name='view-mentors-request'),
    path('approve/<int:mentor_id>/', views.approve_mentor_request, name='approve_mentor_request'),
    path('reject/<int:mentor_id>/', views.reject_mentor_request, name='reject_mentor_request'),

    #course video section
    path('videos/', views.VideoListCreateView.as_view(), name='video-list-create'),#playlist clicking video show url
    # path('videos/<int:playlist_id>/', views.VideoDetailView.as_view(), name='video-detail'),
    path('playlists/', views.PlaylistListCreateView.as_view(), name='playlist-list-create'),#playlist showing url
    path('playlists/<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist-detail'),
    path('playlists/<int:pk>/delete/', views.PlaylistDeleteView.as_view(), name='playlist-delete'),
    path('videos/<int:pk>/delete/', views.VideoDeleteView.as_view(), name='video-delete'),
    
    path('playlists/create/', views.PlaylistListCreateView.as_view(), name='playlist-create'),
    path('videos/create/', views.VideoCreateView.as_view(), name='video-create'),

    path('get-mentor-id/<int:user_id>/', views.get_mentor_id, name='get_mentor_id'),
    path('user-playlists/', views.PlaylistList.as_view(), name='playlist-list'),
    path('get-user/<int:user_id>/', views.get_user, name='get-user'),

    path('playlist-videos/<int:playlist_id>/', views.playlist_videos, name='playlist-videos'),
   
    # path('ws/',include(websocket_urlpatterns))

]