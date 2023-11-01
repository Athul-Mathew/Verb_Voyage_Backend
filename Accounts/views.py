from django.shortcuts import render,redirect
from django.contrib.auth import logout
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import json
from decouple import config

BACKEND_BASE_URL ='https://verbvoyage-frontend-srmq.vercel.app'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.name
        token['is_admin']=user.is_admin
        token['is_staff']=user.is_staff
        token['is_premium']=user.is_premium

        


        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer 

@api_view(["GET"])
def getRoutes(request):
    routes = [
        "api/login",
    ]
    return Response(routes)

class UserRegistration(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        serializer = UserRegisterSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.set_password(password)
            
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('account_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'cite': current_site
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({'status': 'success', 'msg': 'A verificaiton link sent to your registered email address', "data": serializer.data})
        else:
            return Response({'status': 'error', 'msg': serializer.errors})

@api_view(['GET'])

def Activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserAccount._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, UserAccount.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        print('saved')

        return HttpResponseRedirect(BACKEND_BASE_URL+'/login')
    
    
def get_user_info(request, user_id):
    user = get_object_or_404(UserAccount, id=user_id)

    # Serialize the user data using the UserSerializer
    serializer = UserSerializer(user)
    serialized_data = serializer.data

    # Include the serialized data in the JsonResponse
    user_data = {
        'name': serialized_data['name'], 
        'email': serialized_data['email'],
        'profile_image': serialized_data['profile_image'],
        # Include other fields as needed
    }

    return JsonResponse(user_data)


@api_view(['GET'])
def get_users(request):
    users = UserAccount.objects.filter(is_admin=False)  
    serialized_users = UserSerializer(users, many=True)
    return Response(serialized_users.data)

@api_view(['GET'])
def get_staff(request):
    users = UserAccount.objects.filter(is_staff=True)  
    serialized_users = UserSerializer(users, many=True)
    return Response(serialized_users.data)

@api_view(['POST'])
def block_user(request, user_id):
    try:
        user = UserAccount.objects.get(id=user_id)
        user.is_active = False  # Deactivate the user
        user.save()
        return JsonResponse({'message': 'User blocked successfully'})
    except UserAccount.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
@api_view(['POST'])
def unblock_user(request, user_id):
    try:
        user = UserAccount.objects.get(id=user_id)
        user.is_active = True  # Activate the user
        user.save()
        return JsonResponse({'message': 'User unblocked successfully'})
    except UserAccount.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    

class ForgotPassword(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')

        if UserAccount.objects.filter(email=email).exists():
            user = UserAccount.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Please reset your password'
            message = render_to_string('reset_password.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response(
                data={
                    'message': 'Password reset email send',
                    'user_id': user.id
                },
                status=status.HTTP_200_OK
            )

            
        else:
            return Response(
                data={'message': 'No account found'},
                status=status.HTTP_404_NOT_FOUND
            )

@api_view(['GET'])
def reset_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserAccount._default_manager.get(pk=uid)
    except (TypeError, ValueError, UserAccount.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):

        return HttpResponseRedirect(BACKEND_BASE_URL+'/reset-password/')
    

class ResetPassword(APIView):
    def post(self, request, format=None):
        str_user_id = request.data.get('user_id')
        
        uid = int(str_user_id)
        
        password = request.data.get('password')

        if uid:
            user = UserAccount.objects.get(id=uid)
            user.set_password(password)
            user.save()

            return Response(data={'message': 'Password reset succesfully'}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, user_id):
        user = UserAccount.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id):
        print(request.data)
        user = UserAccount.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(user).data)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    
# @api_view(['GET'])
# def UserProfileView1(request,user_id):
#     user = get_object_or_404(UserAccount,id = user_id)
    
#     serializer = UserSerializer(user)
#     return Response(serializer.data)