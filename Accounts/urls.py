from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('signup/', views.UserRegistration.as_view()),
    path('', views.getRoutes, name='get_routes'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('activate/<uidb64>/<token> ', views.Activate, name='activate'),
     path('users/<int:user_id>/', views.get_user_info, name='get_user_info'),
     path('users/', views.get_users, name='get_users'),
    
     path('staff/', views.get_staff, name='staff'),
     path('staff/<int:id>', views.get_staff, name='staff'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('forgot-password/', ForgotPassword.as_view()),
    path('reset-validate/<uidb64>/<token> ',
         views.reset_validate, name='reset_validate'),
    path('reset-password/', ResetPassword.as_view()),

        path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('editusers/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
]
