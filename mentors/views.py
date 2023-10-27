from django.shortcuts import render
from Accounts.models import *
from rest_framework import generics
from .models import Video, Playlist
from .serializers import VideoSerializer, PlaylistSerializer
# Create your views here.
# views.py
from django.core.mail import send_mail

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Mentor
from .serializers import MentorApplicationSerializer, MentorSerializer







@api_view(['POST'])
def create_mentor(request):
    
    if request.method == 'POST':
        serializer = MentorSerializer(data=request.data)
        if serializer.is_valid():
           
            serializer.save(is_active=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_mentors(request):
    mentors = Mentor.objects.filter(is_active=True)
    
    mentor_data = [
        {
            'name': mentor.name,
            
            'image_url': mentor.image.url, 
        }
        for mentor in mentors
    ]
    
    return JsonResponse({'mentors': mentor_data})

@api_view(['POST'])
def mentor_application_view(request):
    
    if request.method == 'POST':
        serializer = MentorApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
def view_mentors(request):
    
    mentors = Mentor.objects.filter(is_active=True)
    serialized_mentors = MentorApplicationSerializer(mentors,many=True)
    return Response(serialized_mentors.data)


@api_view(['GET'])
def view_mentors_request(request):

    mentors = Mentor.objects.filter(is_active=False)
    serialized_mentor_requests = MentorApplicationSerializer(mentors,many = True)
    return Response(serialized_mentor_requests.data)

@api_view(['POST'])
def approve_mentor_request(request, mentor_id):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    user = mentor.user

    user.is_staff = True
    user.save()

    mentor.is_active = True
    mentor.save()

    # Send email to the user
    subject = 'Mentor Request Approved'
    message = 'Your mentor request has been approved. You are now a mentor please logout your account and login again to work as a mentor.'
    from_email = 'verbvoyage2023@gmail.com'
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)

    # Send notification to the user's channel layer group
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications_group',
        {'type': 'send_notification', 'message': 'mentor_request_approved'}
    )
    response_data = {'message': 'mentor request approved success', 'mentor_approved': True}
    return Response(response_data)


@api_view(['POST'])
def reject_mentor_request(request, mentor_id):
    # Get the mentor instance by ID
    mentor = get_object_or_404(Mentor, id=mentor_id)

    
    
    mentor.delete()


    return Response({'message': 'Mentor request rejected and mentor deleted successfully'})





# course playlist section
class VideoListCreateView(generics.ListCreateAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        playlist_id = self.request.query_params.get('playlist_id')
        queryset = Video.objects.filter(mentor__user_id=user_id, playlist_id=playlist_id)
        return queryset

class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VideoSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter videos for the current user
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Video.objects.filter(mentor_id=user_id)
        return Video.objects.none()

class PlaylistListCreateView(generics.ListCreateAPIView):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        
        if user_id:
            return Playlist.objects.filter(user_id=user_id)
            
        return Playlist.objects.none()

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')  # Assuming user_id is part of the request data
        serializer.save(user_id=user_id)

    


class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlaylistSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter playlists for the current user
        print("============", user_id)

        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Playlist.objects.filter(user_id=user_id)
        return Playlist.objects.none()
    

class PlaylistDeleteView(generics.DestroyAPIView):
 

    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    # permission_classes = [IsAuthenticated]


class VideoDeleteView(generics.DestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    # permission_classes = [IsAuthenticated]

      



class VideoCreateView(generics.CreateAPIView):
    serializer_class = VideoSerializer
    
    def create(self, request, *args, **kwargs):
        print("00000000000")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            print("Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_mentor_id(request, user_id):
    user = get_object_or_404(UserAccount, id=user_id)
    mentor_id = user.mentor.id  # Adjust this line based on your actual model structure

    return JsonResponse({'mentor_id': mentor_id})

class PlaylistList(generics.ListAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

def get_user(request,user_id):
    user = get_object_or_404(UserAccount, id=user_id)
    return JsonResponse({'user':user})



#video showing in the user side when clicking the playlist
def playlist_videos(request, playlist_id):
    
    playlist = get_object_or_404(Playlist, id=playlist_id)

    
    videos = Video.objects.filter(playlist=playlist)

    
    serializer = VideoSerializer(videos, many=True)
    serialized_data = serializer.data

    return JsonResponse(serialized_data, safe=False)


@api_view(['GET'])
def mentorView(request,user_id):
    user = get_object_or_404(UserAccount,id = user_id)
    
    serializer = MentorSerializer(user)
    
    response_data={
        'user':serializer.data
    }
    return Response(response_data)


